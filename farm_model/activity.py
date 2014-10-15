# TODO: think about fixed costs and non-linear (economies of scale)
# TODO: include equipment

# http://www.vinelandgrowers.com/index.php?p=Our_Fruit#Peaches
# http://eap.mcgill.ca/MagRack/BAH/BAH%202.htm econ of fruit production



activities = {
	 # Fresh, mid August, freestone.
    'peachesRedhavenConventional': {
        'equipment': ['tractor'],
        'times': {
        	'certificationDelayYears': 0,
        	 'harvestStartYear': 7,
        	 'harvestEndYear':	30,
            'harvestStartWeek': 33, 	# mid august for 3 weeks?
            'havestEndWeek': 36,
            'shelfLifeWeeks': 1, 		# weeks from picking
        	},
        'products': {
            'peachesRedhaven': 35, 		# total tons per km^2/year
            'nitrogen': -10,		# kg per km^2/year
            'carbon': 20,		# tons per km^2/year
            'soil': -0.001,		# inches per km^2/year
            'labour': -200,		# hours per km^2/year
            'certification': 0,
            },
        'color': 'red',
        },
    'peachesRedhavenOrganic': {
        'equipment': ['tractor'],
        'times': {
        	'certificationDelayYears': 3,
        	 'harvestStartYear': 7,
        	 'harvestEndYear':	30,
            'harvestStartWeek': 33, 	# mid august for 3 weeks?
            'havestEndWeek': 36,
            'shelfLifeWeeks': 1, 		# weeks from picking
        	},
        'products': {
            'peachesOrganicRedhaven': 30, 		# total tons per km^2?
            'nitrogen': 0,
            'carbon': 10,		# tons per km^2?
            'soil': 0.001,		# inches per km^2?
            'labour': -220,		# hours per km^2/year
            'certification': 1000, # $/farm
            },
        'color': 'pink',
        },

	 # Canning, late August, freestone.
    'peachesBabyGoldConventional': {
        'equipment': ['tractor'],
        'times': {
        	'certificationDelayYears': 0,
        	 'harvestStartYear': 7,
        	 'harvestEndYear':	30,
            'harvestStartWeek': 35, 	# late august for 3 weeks?
            'havestEndWeek': 38,
            'shelfLifeWeeks': 1, 		# weeks from picking
        	},
        'products': {
            'peachesBabyGold': 35, 		# total tons per km^2/year
            'nitrogen': -10,		# kg per km^2/year
            'carbon': 20,		# tons per km^2/year
            'soil': -0.001,		# inches per km^2/year
            'labour': -200,		# hours per km^2/year
            'certification': 0,
            },
        'color': 'yellow',
        },
    'peachesBabyGoldOrganic': {
        'equipment': ['tractor'],
        'times': {
        	'certificationDelayYears': 3,
        	 'harvestStartYear': 7,
        	 'harvestEndYear':	30,
            'harvestStartWeek': 35, 	# late august for 3 weeks?
            'havestEndWeek': 38,
            'shelfLifeWeeks': 1, 		# weeks from picking
        	},
        'products': {
            'peachesOrganicBabyGold': 30, 		# total tons per km^2?
            'nitrogen': 0,
            'carbon': 10,		# tons per km^2?
            'soil': 0.001,		# inches per km^2?
            'labour': -220,		# hours per km^2/year
            'certification': 1000, # $/farm
            },
        'color': 'gold',
        },
	 # Coronation seedless grapes, mid August through to end of September.
    'grapesCoronationConventional': {
        'equipment': ['tractor'],
        'times': {
        	'certificationDelayYears': 0,
        	 'harvestStartYear': 3,		# check
        	 'harvestEndYear':	30,
            'harvestStartWeek': 35, 	# late august for 3 weeks?
            'havestEndWeek': 38,
            'shelfLifeWeeks': 1, 		# weeks from picking
        	},
        'products': {
            'grapes': 35, 		# total tons per km^2/year
            'nitrogen': -10,		# kg per km^2/year
            'carbon': 20,		# tons per km^2/year
            'soil': -0.001,		# inches per km^2/year
            'labour': -200,		# hours per km^2/year
            'certification': 0,
            },
        'color': 'purple',
        },
    }

import random
class Normal:
    def __init__(self, mean, sd):
        self.mean = mean
        self.sd = sd
    def value(self):
        return random.gauss(self.mean, self.sd)
    def __mul__(self, scale):
        return Normal(self.mean*scale, self.sd*scale)



aggregate_measures = {
    'money': {
        #'duramSeed': Normal(50,10),
        'peachesRedhaven': Normal(55,10),
        #'duramSeedOrganic': Normal(55,10),
        'labour': Normal(5,1),
        'certification': Normal(1,0),
        },
    'environment': {
        'carbon': Normal(10,0),
        'nitrogen': Normal(10,10),
        'soil':Normal(10,10),
        'biodiversity':Normal(10,100)
        },
    }



class Activity:
    def __init__(self, name, equipment, products, aggregate_measures, times,
                    color):
        self.name = name
        self.equipment = equipment
        self.products = products
        self.aggregate_measures = aggregate_measures
        self.times = times
        self.color = color

    def get_product(self, key, farm):
        if key in self.products.keys():
            return self.products[key]*farm.area
        elif key in self.aggregate_measures.keys():
            total = 0
            for item, distribution in self.aggregate_measures[key].items():
                if item in self.products.keys():
                    weight = distribution.value()
                    total += weight*self.products[item]*farm.area
            return total

        raise Exception('Could not find product "%s"'%key)

class Activities:
    def __init__(self):
        self.aggregates = dict(aggregate_measures)

        self.activities = []
        for name, data in activities.items():
            self.activities.append(Activity(name, aggregate_measures=self.aggregates, **data))

    def keys(self):
        return [a.name for a in self.activities]

if __name__=='__main__':
    activities = Activities()
