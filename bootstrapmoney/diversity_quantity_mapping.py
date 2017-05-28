# def create_diversity_quantity_mapping(n):
#
#     mapping = [1]
#
#     f = lambda x: 2 * (x + 1) ** 2
#
#     for raw, diversity in enumerate(range(n - 1, 0, -1)):
#         previous_quantity_of_production = mapping[-1] * (diversity + 1)
#         result = round((previous_quantity_of_production + f(raw)) / diversity)
#         mapping.append(result)
#     mapping.append(0)
#     mapping.reverse()
#
#     return mapping


def create_diversity_quantity_mapping(n):

    mapping = [1]

    for raw, diversity in enumerate(range(n - 1, 0, -1)):
        previous_quantity_of_production = mapping[-1] * (diversity + 1)
        result = round((previous_quantity_of_production + 1 * previous_quantity_of_production) / diversity)
        mapping.append(result)
    mapping.append(0)
    mapping.reverse()

    return mapping


if __name__ == "__main__":

    print(create_diversity_quantity_mapping(10))
