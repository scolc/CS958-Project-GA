import ga_solver
import math
import matplotlib.pyplot as plt
import unittest


def f_1(p: list) -> float:
    """
    The simplest possible test function, which returns the input variable.
    """
    return p[0]


def f_2(p: list) -> float:
    """
    A function that expects four input parameters and returns
    a fitness value.
    """
    result = (p[1]**2 + p[2])
    result += math.cos(p[3])*p[0] + p[1]**2
    return result


class TestSolutionPoint(unittest.TestCase):
    def test_evaluation(self):
        """
        Test the evaluate function.
        """

        parameters = [
            1
        ]
        point = ga_solver.SolutionPoint(f_1, parameters, generation_id=1)
        generation_id = 1
        point.evaluate(generation_id)
        self.assertEqual(point.generation_id, generation_id)
        self.assertEqual(point.fitness, parameters[0])

    def test_create(self):
        """
        Test the create function.
        """

        parameters_1 = [
            1,
            5.5
        ]
        point_1 = ga_solver.SolutionPoint(f_1, parameters_1, generation_id=1)
        parameters_2 = [
            5,
            10.2
        ]
        point_2 = ga_solver.SolutionPoint(f_1, parameters_2, generation_id=1)
        point_3 = point_1.create([point_2], generation_id=2)

        n_parameters = len(parameters_1)
        for i in range(n_parameters):

            # The test data must use the same type for the test to be valid.
            self.assertTrue(type(point_1.parameters[i]),
                            type(point_2.parameters[i]))

            # Find the minimum and the maximum.
            min_value = min([point_1.parameters[i], point_2.parameters[i]])
            max_value = max([point_1.parameters[i], point_2.parameters[i]])

            # Check the point is within the limits.
            self.assertGreaterEqual(point_3.parameters[i], min_value)
            self.assertLessEqual(point_3.parameters[i], max_value)

        # Check the type.
        self.assertTrue(isinstance(point_3.parameters[i], type(min_value)))


class TestGaSolver(unittest.TestCase):
    def test_initialise(self):
        """
        Test the initialise function.
        """

        # Define limits for each parameter.
        limits = [
            (1, 10, int),  # min, max, type
            (2, 3, float)  # min, max, type
        ]
        solver = ga_solver.GaSolver(f_1, limits)
        population_size = 10
        solver.initialise(population_size)

        # Check the population size.
        self.assertEqual(len(solver.population), population_size)
        n_limits = len(limits)
        for point in solver.population:

            # Check the number of parameters.
            self.assertEqual(n_limits, len(point.parameters))
            for i in range(n_limits):

                # Check the points are within the limits.
                self.assertGreaterEqual(point.parameters[i], limits[i][0])
                self.assertLessEqual(point.parameters[i], limits[i][1])

                # Check the type.
                self.assertTrue(isinstance(point.parameters[i], limits[i][2]))

    def test_delete(self) -> int:
        """
        Test the delete function.
        """
        solver = ga_solver.GaSolver(f_1, limits=[], deletion=0.75)
        solver.population.append(ga_solver.SolutionPoint(solver.f,
                                                         [0, 0],
                                                         generation_id=0))
        solver.population.append(ga_solver.SolutionPoint(solver.f,
                                                         [1, 0],
                                                         generation_id=0))
        solver.population.append(ga_solver.SolutionPoint(solver.f,
                                                         [1, 1],
                                                         generation_id=0))
        solver.population.append(ga_solver.SolutionPoint(solver.f,
                                                         [2, 1],
                                                         generation_id=0))
        n_delete = solver.delete()
        self.assertEqual(n_delete, 3)
        self.assertEqual(len(solver.population), 1)
        self.assertEqual(solver.population[0].parameters[0], 2)
        self.assertEqual(solver.population[0].parameters[1], 1)

    def test_create_points(self):
        """
        Test the create_points function.
        """
        solver = ga_solver.GaSolver(f_1, limits=[], n_parents=3)
        solver.population.append(ga_solver.SolutionPoint(solver.f,
                                                         [0, 0],
                                                         generation_id=0))
        solver.population.append(ga_solver.SolutionPoint(solver.f,
                                                         [5, 5],
                                                         generation_id=0))
        solver.population.append(ga_solver.SolutionPoint(solver.f,
                                                         [3, 7],
                                                         generation_id=0))
        n_points = solver.create_points(2, 1)
        self.assertTrue(n_points, 2)
        self.assertGreaterEqual(solver.population[3].parameters[0], 0)
        self.assertLessEqual(solver.population[3].parameters[0], 5)
        self.assertGreaterEqual(solver.population[4].parameters[0], 0)
        self.assertLessEqual(solver.population[4].parameters[0], 5)
        self.assertGreaterEqual(solver.population[4].parameters[1], 0)
        self.assertLessEqual(solver.population[4].parameters[1], 7)
        self.assertGreaterEqual(solver.population[4].parameters[1], 0)
        self.assertLessEqual(solver.population[4].parameters[1], 7)

    def test_mutate(self):
        """
        Test the mutate function.
        """

        limits = [
            (0, 3, int),
            (0, 5, int)
        ]
        solver = ga_solver.GaSolver(f_1, limits, mutation=1.0, n_mutations=2)
        solver.population.append(ga_solver.SolutionPoint(solver.f,
                                                         [0, 0],
                                                         generation_id=0))
        solver.population.append(ga_solver.SolutionPoint(solver.f,
                                                         [1, 0],
                                                         generation_id=0))
        solver.population.append(ga_solver.SolutionPoint(solver.f,
                                                         [1, 1],
                                                         generation_id=0))
        solver.population.append(ga_solver.SolutionPoint(solver.f,
                                                         [2, 1],
                                                         generation_id=0))
        solver.population[0].score = 0
        solver.population[1].score = 1
        solver.population[2].score = 0
        solver.population[3].score = 1
        ga_solver.GaSolver.set_seed(1234567)
        n_mutations_generated = solver.mutate(1)
        self.assertTrue(n_mutations_generated > 0)
        self.assertEqual(solver.population[1].parameters[0], 1)
        self.assertEqual(solver.population[1].parameters[1], 0)
        self.assertEqual(solver.population[1].generation_id, 1)
        self.assertEqual(solver.population[3].parameters[0], 2)
        self.assertEqual(solver.population[3].parameters[1], 2)
        self.assertEqual(solver.population[3].generation_id, 1)

    def test_solve(self):
        """
        A function to verify that the solver is functioning correctly.
        """

        # Set the limits
        limits = [
            (0, 1, float),
            (0, 1, float),
            (0, 1, float),
            (0, 1, float)
        ]

        # Run the solver, with the more complex test function.
        ga_solver.GaSolver.set_seed(1234567)
        solver = ga_solver.GaSolver(f_2, limits=limits, enable_history=True)
        exit_status = solver.solve()
        self.assertEqual(exit_status, 0)

        # Loop over the generations and copy the values.
        n = len(solver.history)
        x = []
        y = []
        for i in range(n):
            for point in solver.history[i]:
                x.append(i)
                y.append(point.fitness)

        plt.scatter(x, y, s=0.2)
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.savefig("solve.png")
        plt.close()


if __name__ == '__main__':
    unittest.main()
