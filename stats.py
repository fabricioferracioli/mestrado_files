# -*- coding: utf-8 -*-
#!/usr/bin/pyhton
#http://academic.emporia.edu/mooredwi/rda/notes10.htm
#http://academic.emporia.edu/mooredwi/rda/notes4.htm
#http://www.westgard.com/lesson40.htm

class Stats:

    def totalVariance(self, distribution):
        sumX = []
        Xbar = []
        Xbar2 = []
        sumX2 = []
        sum_squares = []
        within_groups_dg_freedom = 0

        for X in distribution:
            sumX.append(sum(X))
            Xbar.append(float(sumX[len(sumX) - 1]) / len(X))
            Xbar2.append(Xbar[len(Xbar) - 1] ** 2)
            sumX2.append(sum([a**2 for a in X]))
            sum_squares.append(sum([(a - Xbar[len(Xbar) - 1])**2 for a in X]))
            within_groups_dg_freedom += len(X) - 1

        within_groups_sum_squares = sum(sum_squares)
        within_groups_variance = within_groups_sum_squares / within_groups_dg_freedom
        grand_mean = sum(Xbar) / len(Xbar)
        variance_means = sum([(a - grand_mean)**2 for a in Xbar])/(len(distribution) - 1)
        among_groups_variance = len(distribution[0]) * variance_means
        f_value = among_groups_variance / within_groups_variance

        total_variance = 0
        for X in distribution:
            for x in X:
                total_variance = (x - grand_mean)**2

        wilk_lambda = within_groups_variance / total_variance

        return {
                'SST': total_variance,
                'SSB': among_groups_variance,
                'SSW': within_groups_variance,
                'fvalue': f_value,
                'wilk_lambda': wilk_lambda
            }