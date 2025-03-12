from dataclasses import dataclass
import math
from typing import List, Tuple, Dict

from adodbapi.ado_consts import adParamReturnValue


@dataclass
class ResourceType:
    RI: int   # Identifiant de la ressource
    RA: int   # Coût d'activation (one-time)
    RP: int   # Coût périodique par tour où la ressource est vivante
    RW: int   # Nombre de tours consécutifs actifs
    RM: int   # Nombre de tours de maintenance après activité
    RL: int   # Cycle de vie total en tours
    RU: int   # Nombre de bâtiments alimentés par tour actif
    RT: str   # Type d'effet spécial (A, B, C, D, E, X)
    RE: int = 0  # Paramètre de l'effet (pourcentage ou capacité, 0 pour X)

@dataclass
class ResourceInstance:
    type: ResourceType      # Type de la ressource
    purchase_turn: int      # Tour d'achat
    effective_RL: int       # Cycle de vie effectif (ajusté par effet C)
    remaining_charge: int = 0  # Stockage pour les accumulateurs (type E)

class Game:
    def __init__(self, D: int, resource_types: List[ResourceType], turn_params: List[Tuple[int,int,int]]):
        self.initial_budget = D
        self.budget = D
        self.resource_types = resource_types
        self.turn_params = turn_params
        self.T = len(turn_params)
        self.current_turn = 0
        self.resource_instances: List[ResourceInstance] = []
        self.total_score = 0  # Le score correspond à la somme des profits de chaque tour

    def simulate_game(self, purchase_strategy) -> int:
        """Simule la partie entière en appliquant la stratégie d'achat fournie pour chaque tour."""
        for t in range(self.T):
            purchases = purchase_strategy(self, t)
            self.simulate_turn(purchases)
        return self.total_score

    def simulate_turn(self, purchases: List[int]) -> None:
        """Simule un tour en traitant les achats, les effets, le calcul du profit et la mise à jour du budget."""
        # Traiter les achats pour le tour courant
        if not self._process_purchases(purchases):
            self.current_turn += 1
            return

        # Paramètres du tour courant
        T_M, T_X, T_R = self.turn_params[self.current_turn]

        # Identifier les ressources vivantes et actives
        alive_resources = self._get_alive_resources()
        active_resources = self._get_active_resources(alive_resources)

        # Calculer les effets spéciaux combinés
        effects = self._calculate_special_effects(active_resources)
        # Appliquer l'effet B aux seuils et l'effet D au profit par bâtiment
        T_M_eff = max(0, math.floor(T_M * (1 + effects['B'])))
        T_X_eff = max(0, math.floor(T_X * (1 + effects['B'])))
        T_R_eff = max(0, math.floor(T_R * (1 + effects['D'])))

        # Calculer le nombre de bâtiments alimentés en appliquant l'effet A sur chaque ressource non accumulateur
        buildings_powered = self._calculate_buildings_powered(active_resources, effects['A'])
        # Traiter les accumulateurs (ressources de type E)
        self._transfer_accumulator_charge()
        buildings_powered = self._process_accumulators(buildings_powered, T_M_eff, T_X_eff)

        # Calcul du profit du tour (profit = min(buildings_powered, T_X_eff) * T_R_eff si le seuil minimal est atteint)
        profit = min(buildings_powered, T_X_eff) * T_R_eff if buildings_powered >= T_M_eff else 0
        self.total_score += profit

        # Coût de maintenance : somme des RP de toutes les ressources vivantes
        maintenance_cost = sum(res.type.RP for res in alive_resources)
        # Mise à jour du budget selon la formule : nouveau budget = budget précédent + profit - maintenance_cost
        self.budget += profit - maintenance_cost

        self.current_turn += 1

    def _process_purchases(self, purchases: List[int]) -> bool:
        """Traite les achats effectués durant le tour courant."""
        total_RA = sum(self.resource_types[RI - 1].RA for RI in purchases)
        if total_RA > self.budget:
            return False
        self.budget -= total_RA
        for RI in purchases:
            resource_type = self.resource_types[RI - 1]
            effective_RL = self._calculate_effective_RL(resource_type)
            instance = ResourceInstance(type=resource_type, purchase_turn=self.current_turn, effective_RL=effective_RL)
            self.resource_instances.append(instance)
        return True

    def _calculate_effective_RL(self, resource_type: ResourceType) -> int:
        """Calcule le cycle de vie effectif d'une ressource en tenant compte des effets de type C."""
        active_C = [res for res in self.resource_instances if res.type.RT == 'C' and self._is_resource_active(res)]
        c_effect = sum(res.type.RE / 100 for res in active_C)
        return max(1, math.floor(resource_type.RL * (1 + c_effect)))

    def _get_alive_resources(self) -> List[ResourceInstance]:
        """Retourne les ressources dont le cycle de vie n'est pas terminé."""
        return [res for res in self.resource_instances if self.current_turn - res.purchase_turn < res.effective_RL]

    def _get_active_resources(self, alive_resources: List[ResourceInstance]) -> List[ResourceInstance]:
        """Retourne les ressources actives au tour courant (c'est-à-dire en phase d'activité)."""
        return [res for res in alive_resources if self._is_resource_active(res)]

    def _is_resource_active(self, resource: ResourceInstance) -> bool:
        local_turn = self.current_turn - resource.purchase_turn
        if local_turn >= resource.effective_RL:
            return False
        cycle_length = resource.type.RW + resource.type.RM
        pos = local_turn % cycle_length
        return pos < resource.type.RW

    def _calculate_special_effects(self, active_resources: List[ResourceInstance]) -> Dict[str, float]:
        """Calcule les effets spéciaux combinés des ressources actives."""
        effects = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': []}
        for res in active_resources:
            if res.type.RT in ['A', 'B', 'C', 'D']:
                effects[res.type.RT] += res.type.RE / 100
            elif res.type.RT == 'E':
                effects['E'].append(res)
        return effects

    def _calculate_buildings_powered(self, active_resources: List[ResourceInstance], a_effect: float) -> int:
        """Calcule le nombre total de bâtiments alimentés par les ressources actives (hors accumulateurs),
        en appliquant l'effet A (Smart Meter)."""
        total = 0
        for res in active_resources:
            if res.type.RT != 'E':
                adjusted_RU = math.floor(res.type.RU * (1 + a_effect))
                total += adjusted_RU
        return total

    def _process_accumulators(self, buildings_powered: int, T_M_eff: int, T_X_eff: int) -> int:
        """Traite les ressources de type E (accumulateurs) pour stocker l'excédent ou compenser un déficit."""
        active_E = [res for res in self.resource_instances if res.type.RT == 'E' and self._is_resource_active(res)]
        if not active_E:
            return buildings_powered
        if buildings_powered > T_X_eff:
            surplus = buildings_powered - T_X_eff
            self._store_in_accumulators(surplus, active_E)
            return T_X_eff
        elif buildings_powered < T_M_eff:
            deficit = T_M_eff - buildings_powered
            compensated = self._discharge_from_accumulators(deficit, active_E)
            return buildings_powered + compensated
        return buildings_powered

    def _store_in_accumulators(self, surplus: int, accumulators: List[ResourceInstance]) -> None:
        total_capacity = sum(res.type.RE for res in accumulators)
        total_stored = sum(res.remaining_charge for res in accumulators)
        available = total_capacity - total_stored
        to_store = min(surplus, available)
        if to_store > 0 and total_capacity > 0:
            for res in accumulators:
                proportion = res.type.RE / total_capacity
                store_amt = min(math.floor(to_store * proportion), res.type.RE - res.remaining_charge)
                res.remaining_charge += store_amt

    def _discharge_from_accumulators(self, deficit: int, accumulators: List[ResourceInstance]) -> int:
        total_available = sum(res.remaining_charge for res in accumulators)
        discharge_amt = min(deficit, total_available)
        if discharge_amt > 0 and total_available > 0:
            for res in accumulators:
                proportion = res.remaining_charge / total_available
                discharge = min(math.floor(discharge_amt * proportion), res.remaining_charge)
                res.remaining_charge -= discharge
        return discharge_amt

    def _transfer_accumulator_charge(self) -> None:
        """Transfère la charge des accumulateurs en fin de vie vers d'autres accumulateurs actifs."""
        expiring = [res for res in self.resource_instances
                    if res.type.RT == 'E' and
                    self.current_turn - res.purchase_turn == res.effective_RL - 1 and
                    res.remaining_charge > 0]
        continuing = [res for res in self.resource_instances
                      if res.type.RT == 'E' and
                      self._is_resource_active(res) and
                      self.current_turn - res.purchase_turn < res.effective_RL - 1]
        for exp in expiring:
            if continuing:
                self._store_in_accumulators(exp.remaining_charge, continuing)
            exp.remaining_charge = 0

def read_input(file_path: str) -> Tuple[int, List[ResourceType], List[Tuple[int, int, int]]]:
    """Lit le fichier d'entrée et retourne le budget initial, la liste des types de ressources et les paramètres des tours."""
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    first_line = lines[0].split()
    D = int(first_line[0])
    R = int(first_line[1])
    T = int(first_line[2])
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
    turn_params = []
    for i in range(R + 1, R + 1 + T):
        parts = lines[i].split()
        T_M = int(parts[0])
        T_X = int(parts[1])
        T_R = int(parts[2])
        turn_params.append((T_M, T_X, T_R))
    return D, resource_types, turn_params

def optimal_purchase_strategy(game: Game, turn: int) -> List[int]:
    """Stratégie d'achat qui évalue l'efficacité de chaque type de ressource
    et tente d'acheter celles qui maximisent le potentiel."""
    available_budget = game.budget
    T_M, T_X, T_R = game.turn_params[turn]
    resource_values = []
    for res in game.resource_types:
        if res.RA > available_budget:
            continue
        # Calculer un ratio simple d'efficacité
        efficiency = res.RA / res.RU if res.RU > 0 else float('inf')
        # Bonus pour les ressources de type A et D
        if res.RT == 'A' and res.RE > 0:
            efficiency *= 1.5
        elif res.RT == 'D' and res.RE > 0:
            efficiency *= 1.5
        # Estimer le nombre de tours actifs et le potentiel de profit
        active_turns = res.RW * (res.RL // (res.RW + res.RM))
        profit_potential = active_turns * res.RU * T_R
        maintenance_cost = res.RL * res.RP
        net_profit = profit_potential - maintenance_cost - res.RA
        if net_profit > 0:
            efficiency *= 1.2
        resource_values.append((res.RI, efficiency, res.RA))
    resource_values.sort(key=lambda x: x[1], reverse=True)
    purchases = []
    for ri, _, ra in resource_values:
        if ra <= available_budget:
            purchases.append(ri)
            available_budget -= ra

    return purchases

def generate_output(game: Game) -> List[str]:
    """Génère la sortie au format attendu, c'est-à-dire une ligne par tour (s'il y a achat),
    puis la dernière ligne contenant le score total."""
    output_lines = []
    for t in range(game.T):
        purchases = [str(res.type.RI) for res in game.resource_instances if res.purchase_turn == t]
        if purchases:
            output_lines.append(f"{t} {len(purchases)} {' '.join(purchases)}")
    return output_lines

if __name__ == "__main__":
    # Lecture de l'input depuis "0-demo.txt"
    D, resource_types, turn_params = read_input("0-demo.txt")
    game = Game(D, resource_types, turn_params)

    # Simuler le jeu en appliquant la stratégie d'achat optimale
    total_score = game.simulate_game(optimal_purchase_strategy)
    print(f"Score total : {total_score}")

    # Générer la sortie (historique des achats par tour)
    output_lines = generate_output(game)

    # Écrire le résultat dans "output.txt"
    with open("AymOutput.txt", "w") as f:
        f.write("\n".join(output_lines))

    print("Résultat écrit dans 'output.txt'")
