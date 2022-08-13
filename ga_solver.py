import copy
import random
from typing import Callable


class SolutionPoint:
    """
    A class to hold a solution point within the space considered.
    The solution point is given a function to evaluate to find the
    fitness, a list of parameter settings and a generation
    identifier.
    """

    def __init__(self,
                 f: Callable,
                 parameters: list,
                 fitness: float = 0.0,
                 generation_id: int = 0) -> None:
        self.f = f
        self.parameters = []
        self.parameters += parameters
        self.fitness = fitness
        self.generation_id = generation_id
        self.evaluate(generation_id)

    def __repr__(self) -> str:
        s = "SolutionPoint("
        s += f"f=" + self.f.__name__ + ","
        s += f"parameters={self.parameters},"
        s += f"fitness={self.fitness},"
        s += f"generation_id={self.generation_id}"
        s += ")"
        return s

    def __eq__(self, other: object) -> bool:
        n = len(self.parameters)
        if n != len(other.parameters):
            return False

        for i in range(n):
            if self.parameters[i] != other.parameters[i]:
                return False
        return True

    def evaluate(self, generation_id: int) -> None:
        """
        A function to calculate the fitness and record which generation
        the fitness was calculated in.
        """
        self.fitness = self.f(self.parameters)
        self.generation_id = generation_id

    def create(self, objects: list, generation_id: int) -> object:
        """
        A function to create a new point, combining this point
        with one or more other points.
        """

        # Must supply at least one other parent.
        if len(objects) == 0:
            return None

        # The number of parameters must be the same.
        n_parameters = len(self.parameters)
        for obj in objects:
            if n_parameters != len(obj.parameters):
                return None

        child_parameters = []
        for i in range(n_parameters):

            # All values for this parameter for the parents.
            values = []
            values.append(self.parameters[i])
            for obj in objects:
                values.append(obj.parameters[i])

            # Find the min and max values.
            min_value = min(values)
            max_value = max(values)

            # If parameter values are the same, cannot generate something else.
            if min_value == max_value:
                child_parameters.append(min_value)
                continue

            # Generate the new value within the limits.
            if isinstance(min_value, int) and isinstance(max_value, int):
                value = random.randint(min_value, max_value)
            else:
                value = random.uniform(min_value, max_value)

            # Append this value.
            child_parameters.append(value)

        # Create the child and return it.
        return SolutionPoint(self.f, child_parameters, generation_id)


class GaSolver:
    """
    A genetic algorithm to solve a one-dimensional equation, providing
    functions to find the minimum or maximum within the limits.
    """
    def __init__(self,
                 f: Callable,  # The function that should be evaluated.
                 limits: list,  # A list of tuples that contain the limits.
                 minimise: bool = True,  # True => minimise, False => maximise
                 n_parents: int = 2,  # The number of parents for GA.
                 deletion: float = 0.4,  # The deletion fraction for GA.
                 mutation: float = 0.1,  # The mutation fraction for GA.
                 n_mutations: int = 1,  # The number of parameters to mutate.
                 enable_history: bool = False) -> None:
        self.population = []
        self.f = f
        self.limits = []
        self.limits += limits
        self.minimise = minimise
        self.n_parents = n_parents
        self.deletion = deletion
        self.mutation = mutation
        self.n_mutations = n_mutations
        self.enable_history = enable_history
        self.history = []

    def __generate_parameter(self, limit):
        """
        A function to generate a random integer or float
        within the limits provided.
        """
        if limit[2] == int:
            value = random.randint(limit[0], limit[1])
        else:
            value = random.uniform(limit[0], limit[1])
        return value

    def __generate_parameters(self) -> list:
        """
        A function to generate parameter values within
        the global limits that are associated with this object.
        """
        parameters = []
        for limit in self.limits:
            value = self.__generate_parameter(limit)
            parameters.append(value)
        return parameters

    def __record_points(self) -> None:
        """
        A function to record the current population.
        """
        self.history.append(copy.deepcopy(self.population))

    def set_seed(seed: int) -> None:
        """
        A function to set the random seed value within this module.
        """
        random.seed(seed)

    def initialise(self, n_initial) -> None:
        """
        Create an initial set of solution points.
        """
        self.population.clear()
        for i in range(n_initial):
            parameters = self.__generate_parameters()
            point = SolutionPoint(self.f, parameters, generation_id=0)
            self.population.append(point)

    def delete(self) -> int:
        """
        A function to remove a fraction of the points that are not in the
        Pareto front.
        """

        # Sort the population by fitness.
        self.population.sort(key=lambda x: x.fitness, reverse=True)

        # Calculate the number to delete.
        n_delete = int(len(self.population) * self.deletion + 0.5)

        # Delete the points.
        del self.population[-n_delete:]

        return n_delete

    def create_points(self, n_points: int, generation_id: int) -> int:
        """
        A function to create up to n_points, using any of the existing
        points as parents.
        """

        all_indices = list(range(len(self.population)))
        if len(all_indices) < self.n_parents:
            print("Warning: number of points is less than number of parents.")
            return 0

        # Create the number of new points requested.
        for i in range(n_points):
            # Use any points, selected at random.
            random.shuffle(all_indices)

            # Collect the parent points.
            points = []
            for j in range(self.n_parents):
                point_index = all_indices[j]
                points.append(self.population[point_index])

            # Create the new point.
            new_point = points[0].create(points[1:], generation_id)
            self.population.append(new_point)

        return n_points

    def mutate(self, generation_id: int) -> int:
        """
        A function to mutate a fraction of the points.
        """
        indices = list(range(len(self.population)))

        # There must be some parameter limits to generate mutations.
        n_limits = len(self.limits)
        if n_limits == 0:
            print("Warning: cannot mutate without parameter limits.")
            return -1

        # The number of points to mutate.
        n_mutate = int(self.mutation * len(indices) + 0.5)

        # Use indices to select points to mutate.
        random.shuffle(indices)

        # Mutate the points.
        for i in range(n_mutate):

            # Get the selected point.
            idx = indices[i]
            point = self.population[idx]

            # Can only mutate all of the parameters.
            n_parameters = len(point.parameters)
            if n_parameters < self.n_mutations:
                print("Warning: more mutations requested than parameters.")
                self.n_mutations = n_parameters

            if n_limits != n_parameters:
                print("Warning: number of limits does not match parameters.")
                print("  Cannot mutate.")
                return -1

            # Create a shuffled list of parameter indices.
            parameter_indices = list(range(n_parameters))
            random.shuffle(parameter_indices)

            # Mutate the parameters.
            for j in range(self.n_mutations):
                parameter_index = parameter_indices[j]

                # Pick a random value, between the limits.
                limit = self.limits[parameter_index]
                value = self.__generate_parameter(limit)
                point.parameters[parameter_index] = value

            # Re-evaluate the point with the new parameter settings.
            point.evaluate(generation_id)
        return n_mutate

    def solve(self, n_iterations: int = 300,
              n_initial_points: int = 100) -> int:
        """
        A function to try to find a solution.  The function should be
        given a number of interations and number of initial points.
        The number of interations are the number of generations that the
        genetic algorithm will run.
        """

        # Create initial population.
        self.population.clear()
        self.history.clear()
        self.initialise(n_initial_points)

        # Record the points if needed.
        if self.enable_history:
            self.__record_points()

        exit_status = 0

        # Generation 0 is used for the initial population.
        for generation_id in range(1, n_iterations+1):

            # Delete a fraction of the population.
            n_deleted = self.delete()

            # If there are no more points in the population.
            if n_deleted == 0:
                exit_status = -1
                break

            # Exit if the correct number of points were not generated.
            if self.create_points(n_deleted, generation_id) != n_deleted:
                exit_status = 1
                break

            # Exit if the mutations cannot be generated.
            if self.mutate(generation_id) < 0:
                exit_status = 2
                break

            # Record the points if needed.
            if self.enable_history:
                self.__record_points()

        return exit_status
