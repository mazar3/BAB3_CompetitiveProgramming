from dataclasses import dataclass
import math
from typing import List, Tuple, Dict


@dataclass
class ResourceType:
    RI: int  # Identifiant de la ressource
    RA: int  # Coût d'activation (one-time)
    RP: int  # Coût périodique par tour où la ressource est vivante
    RW: int  # Nombre de tours consécutifs actifs
    RM: int  # Nombre de tours de maintenance après activité
    RL: int  # Cycle de vie total en tours
    RU: int  # Nombre de bâtiments alimentés par tour actif
    RT: str  # Type d'effet spécial (A, B, C, D, E, X)
    RE: int = 0  # Paramètre de l'effet (pourcentage ou capacité, 0 pour X)


@dataclass
class ResourceInstance:
    type: ResourceType  # Type de la ressource
    purchase_turn: int  # Tour d'achat
    effective_RL: int  # Cycle de vie effectif (ajusté par effet C)
    remaining_charge: int = 0  # Stockage pour type E uniquement


class Game:
    def __init__(self, D, resource_types, turn_params):
        self.initial_budget = D
        self.budget = D
        self.resource_types = resource_types
        self.turn_params = turn_params
        self.T = len(turn_params)
        self.current_turn = 0
        self.resource_instances = []
        self.total_score = 0
        self.turn_history = []  # Pour le débogage

    def simulate_game(self, purchase_strategy):
        """Simule le jeu entier avec la stratégie fournie."""
        for t in range(self.T):
            purchases = purchase_strategy(self, t)
            self.simulate_turn(purchases)
        return self.total_score

    def simulate_turn(self, purchases):
        """Simule un tour de jeu."""
        # Valider et traiter les achats
        if not self._process_purchases(purchases):
            self.current_turn += 1
            return False

        # Obtenir les paramètres du tour
        T_M, T_X, T_R = self.turn_params[self.current_turn]

        # Traiter les ressources actives et leurs effets
        alive_resources = self._get_alive_resources()
        active_resources = self._get_active_resources(alive_resources)

        # Calculer les effets spéciaux
        effects = self._calculate_special_effects(active_resources)

        # Appliquer les effets aux paramètres du tour
        T_M_eff = max(0, math.floor(T_M * (1 + effects['B'])))
        T_X_eff = max(0, math.floor(T_X * (1 + effects['B'])))
        T_R_eff = max(0, math.floor(T_R * (1 + effects['D'])))

        # Calculer le nombre total de bâtiments alimentés
        buildings_powered = self._calculate_buildings_powered(active_resources, effects['A'])

        # Traiter les ressources de type E (accumulateurs)
        self._transfer_accumulator_charge()  # Transférer la charge des accumulateurs qui expirent
        buildings_powered = self._process_accumulators(buildings_powered, T_M_eff, T_X_eff)

        # Calculer le profit
        if buildings_powered >= T_M_eff:
            profit = min(buildings_powered, T_X_eff) * T_R_eff
        else:
            profit = 0

        # Calculer les coûts de maintenance
        maintenance_cost = sum(res.type.RP for res in alive_resources)

        # Mettre à jour le budget et le score
        self.budget += profit - maintenance_cost
        self.total_score += profit

        # Passer au tour suivant
        self.current_turn += 1
        return True

    def _process_purchases(self, purchases):
        """Traite les achats de ressources pour le tour actuel."""
        # Calculer le coût total d'activation
        total_RA = sum(self.resource_types[RI - 1].RA for RI in purchases)

        # Vérifier si le budget est suffisant
        if total_RA > self.budget:
            return False

        # Déduire le coût d'activation du budget
        self.budget -= total_RA

        # Créer des instances de ressources pour chaque achat
        for RI in purchases:
            resource_type = self.resource_types[RI - 1]

            # Calculer le cycle de vie effectif basé sur les ressources C actives
            effective_RL = self._calculate_effective_RL(resource_type)

            # Créer et ajouter l'instance de ressource
            res_instance = ResourceInstance(
                type=resource_type,
                purchase_turn=self.current_turn,
                effective_RL=effective_RL
            )
            self.resource_instances.append(res_instance)

        return True

    def _calculate_effective_RL(self, resource_type):
        """Calcule le cycle de vie effectif en considérant les effets de type C."""
        active_C_resources = [
            res for res in self.resource_instances
            if res.type.RT == 'C' and self._is_resource_active(res)
        ]

        # Sommer tous les effets de type C (positifs et négatifs)
        c_effect = sum(res.type.RE / 100 for res in active_C_resources)

        # Appliquer l'effet au RL, valeur minimale est 1
        effective_RL = max(1, math.floor(resource_type.RL * (1 + c_effect)))
        return effective_RL

    def _get_alive_resources(self):
        """Obtenir toutes les ressources encore dans leur cycle de vie."""
        return [
            res for res in self.resource_instances
            if self.current_turn - res.purchase_turn < res.effective_RL
        ]

    def _get_active_resources(self, alive_resources):
        """Obtenir toutes les ressources actives dans le tour actuel."""
        return [
            res for res in alive_resources
            if self._is_resource_active(res)
        ]

    def _is_resource_active(self, resource):
        """Vérifier si une ressource est active dans le tour actuel."""
        local_turn = self.current_turn - resource.purchase_turn

        if local_turn >= resource.effective_RL:
            return False

        # Calculer la position dans le cycle d'activité
        cycle_length = resource.type.RW + resource.type.RM
        position_in_cycle = local_turn % cycle_length

        # La ressource est active si elle est dans sa période active
        return position_in_cycle < resource.type.RW

    def _calculate_special_effects(self, active_resources):
        """Calculer les effets spéciaux combinés de toutes les ressources actives."""
        effects = {
            'A': 0,  # Smart Meter effect
            'B': 0,  # Distribution Facility effect
            'C': 0,  # Maintenance Plan effect
            'D': 0,  # Renewable Plant effect
            'E': []  # Accumulator resources
        }

        for res in active_resources:
            if res.type.RT in ['A', 'B', 'C', 'D']:
                # Ajouter l'effet (positif ou négatif)
                effects[res.type.RT] += res.type.RE / 100
            elif res.type.RT == 'E':
                effects['E'].append(res)

        return effects

    def _calculate_buildings_powered(self, active_resources, a_effect):
        """Calculer le nombre total de bâtiments alimentés par toutes les ressources actives."""
        total_buildings = 0

        for res in active_resources:
            if res.type.RT != 'E':  # Les ressources de type E n'alimentent pas directement les bâtiments
                # Appliquer l'effet A à chaque ressource
                adjusted_RU = math.floor(res.type.RU * (1 + a_effect))
                total_buildings += adjusted_RU

        return total_buildings

    def _process_accumulators(self, buildings_powered, T_M_eff, T_X_eff):
        """Traiter les ressources de type E (accumulateurs)."""
        active_E_resources = [
            res for res in self.resource_instances
            if res.type.RT == 'E' and self._is_resource_active(res)
        ]

        # Si pas d'accumulateurs actifs, retourner le nombre original de bâtiments
        if not active_E_resources:
            return buildings_powered

        # Traiter le stockage excédentaire
        if buildings_powered > T_X_eff:
            surplus = buildings_powered - T_X_eff
            self._store_in_accumulators(surplus, active_E_resources)
            return T_X_eff

        # Traiter la compensation de déficit
        elif buildings_powered < T_M_eff:
            deficit = T_M_eff - buildings_powered
            compensated = self._discharge_from_accumulators(deficit, active_E_resources)
            return buildings_powered + compensated

        return buildings_powered

    def _store_in_accumulators(self, surplus, accumulators):
        """Stocker les bâtiments excédentaires dans les accumulateurs actifs."""
        # Calculer la capacité totale et l'espace disponible
        total_capacity = sum(res.type.RE for res in accumulators)
        total_stored = sum(res.remaining_charge for res in accumulators)
        available_capacity = total_capacity - total_stored

        # Stocker seulement ce qui peut tenir
        to_store = min(surplus, available_capacity)

        # Distribuer le stockage proportionnellement à la capacité
        if to_store > 0 and total_capacity > 0:
            for res in accumulators:
                proportion = res.type.RE / total_capacity
                res_storage = min(math.floor(to_store * proportion), res.type.RE - res.remaining_charge)
                res.remaining_charge += res_storage

    def _discharge_from_accumulators(self, deficit, accumulators):
        """Décharger les bâtiments stockés pour compenser un déficit."""
        total_available = sum(res.remaining_charge for res in accumulators)
        discharge_amount = min(deficit, total_available)

        # Distribuer la décharge proportionnellement
        if discharge_amount > 0 and total_available > 0:
            for res in accumulators:
                proportion = res.remaining_charge / total_available
                res_discharge = min(math.floor(discharge_amount * proportion), res.remaining_charge)
                res.remaining_charge -= res_discharge

        return discharge_amount

    def _transfer_accumulator_charge(self):
        """Transférer la charge des accumulateurs en fin de vie vers d'autres accumulateurs actifs."""
        # Trouver les accumulateurs qui expireront à ce tour
        expiring_accumulators = [
            res for res in self.resource_instances
            if res.type.RT == 'E'
               and self.current_turn - res.purchase_turn == res.effective_RL - 1
               and res.remaining_charge > 0
        ]

        # Trouver les accumulateurs actifs qui continueront au tour suivant
        continuing_accumulators = [
            res for res in self.resource_instances
            if res.type.RT == 'E'
               and self._is_resource_active(res)
               and self.current_turn - res.purchase_turn < res.effective_RL - 1
        ]

        # Transférer la charge
        for expiring in expiring_accumulators:
            if continuing_accumulators:
                self._store_in_accumulators(expiring.remaining_charge, continuing_accumulators)
            expiring.remaining_charge = 0


def read_input(file_path):
    """Lire et analyser le fichier d'entrée."""
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # Analyser la première ligne
    first_line = lines[0].split()
    D = int(first_line[0])
    R = int(first_line[1])
    T = int(first_line[2])

    # Analyser les types de ressources
    resource_types = []
    for i in range(1, R + 1):
        parts = lines[i].split()
        RI = int(parts[0])
        RA = int(parts[1])
        RP = int(parts[2])
        RW = int(parts[3])
        RM = int(parts[4])
        RL = int(parts[5])
        RU = int(parts[6])
        RT = parts[7]
        RE = 0 if RT == 'X' else int(parts[8])
        resource_types.append(ResourceType(RI, RA, RP, RW, RM, RL, RU, RT, RE))

    # Analyser les paramètres des tours
    turn_params = []
    for i in range(R + 1, R + 1 + T):
        parts = lines[i].split()
        T_M = int(parts[0])
        T_X = int(parts[1])
        T_R = int(parts[2])
        turn_params.append((T_M, T_X, T_R))

    return D, resource_types, turn_params


def optimal_purchase_strategy(game, turn):
    """Stratégie d'achat qui maximise l'efficacité des ressources."""
    available_budget = game.budget
    T_M, T_X, T_R = game.turn_params[turn]

    # Calculer le rapport valeur/coût pour chaque ressource
    resource_values = []
    for resource in game.resource_types:
        # Ignorer les ressources qui coûtent plus que notre budget
        if resource.RA > available_budget:
            continue

        # Calculer le ratio valeur/coût et tenir compte des effets spéciaux
        efficiency = resource.RU / resource.RA if resource.RA > 0 else float('inf')

        # Ajuster l'efficacité en fonction du type de ressource
        if resource.RT == 'A' and resource.RE > 0:  # Bonus de Smart Meter positif
            efficiency *= 1.5
        elif resource.RT == 'D' and resource.RE > 0:  # Bonus de profit positif
            efficiency *= 1.5

        # Considérer la durée de vie et les coûts de maintenance
        active_turns = resource.RW * (resource.RL // (resource.RW + resource.RM))
        profit_potential = active_turns * resource.RU * T_R
        maintenance_cost = resource.RL * resource.RP
        net_profit = profit_potential - maintenance_cost - resource.RA

        # Valoriser davantage les ressources avec un profit net positif
        if net_profit > 0:
            efficiency *= 1.2

        resource_values.append((resource.RI, efficiency, resource.RA))

    # Trier par efficacité (décroissant)
    resource_values.sort(key=lambda x: x[1], reverse=True)

    # Acheter autant de ressources à haute valeur que possible
    purchases = []
    for ri, _, ra in resource_values:
        if ra <= available_budget:
            purchases.append(ri)
            available_budget -= ra

    return purchases


def generate_output(game):
    """Générer le format de sortie basé sur l'historique du jeu."""
    output_lines = []

    for t in range(game.T):
        purchases = [ri.type.RI for ri in game.resource_instances if ri.purchase_turn == t]
        if purchases:
            output_lines.append(f"{t} {len(purchases)} {' '.join(map(str, purchases))}")

    return output_lines


# Exécution principale
if __name__ == "__main__":
    D, resource_types, turn_params = read_input("0-demo.txt")
    game = Game(D, resource_types, turn_params)

    # Exécuter le jeu avec une stratégie optimisée
    total_score = game.simulate_game(optimal_purchase_strategy)

    print(f"Score total : {total_score}")

    # Générer la sortie
    output = generate_output(game)
    for line in output:
        print(line)