from models import *

categorylist = ['beach','boat_tour','cruise','fishing_charter','forest','general','hiking',
 'horse_riding','island','jet_tour','sailing','scenic_flight_tour',
 'scuba_diving','scuba_doo','sky_diving','snorkeling','snorkeling_tour',
 'submarine_creature','surfing','swimming','valley','waterfall',
 'watersport','whale_watching']
print (len(categorylist))

for i in range(len(categorylist)):
    cat = Category(id=i,name=categorylist[i].decode('utf-8'))
    db.session.add(cat)
    db.session.commit()