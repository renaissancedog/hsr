from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def air(mi):
    return .11*mi+250
def road(mi):
    return mi+30
def hsr(mi):
    return .36*mi+60
def triple_point():
    # solve for when air = road
    mi = (250-30)/(1-.11)
    return mi
def time_diff(mi):
    if (hsr(mi) < air(mi) and hsr(mi) < road(mi)):
        return min(air(mi)-hsr(mi), road(mi)-hsr(mi))
    else:
        return 0
max_time_diff = time_diff(triple_point())
def multiplier(mi):
    time=time_diff(mi)
    return time/max_time_diff
def plot():
    minutes = np.arange(0, 60*20+1, 60)
    air_costs = [air(mi) for mi in minutes]
    road_costs = [road(mi) for mi in minutes]
    hsr_costs = [hsr(mi) for mi in minutes]
    plt.figure(figsize=(10,10))
    plt.plot(minutes, air_costs, label='Air')
    plt.plot(minutes, road_costs, label='Road')
    plt.plot(minutes, hsr_costs, label='HSR')
    plt.xlabel('Miles')
    plt.ylabel('Minutes')
    plt.title('Distance vs Time for Different Transportation Methods')
    plt.legend()
    plt.grid()
    plt.savefig("distance_vs_time.png")

def haversine(lon1, lat1, lon2, lat2):
    # distance btw 2 coordnates assuming earth is a sphere, miles
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    return 3963 * c

gravity_threshold=10

def main():
    msa_df=pd.read_csv("msa.csv")
    data=[]
    for i in range(len(msa_df)):
        for j in range(i+1, len(msa_df)):
            city1=msa_df.iloc[i]
            city2=msa_df.iloc[j]
            mi=haversine(city1['lon'], city1['lat'], city2['lon'], city2['lat'])
            mult=multiplier(mi)
            gravity_score=mult*(city1['pop']/1000)*(city2['pop']/1000)/(mi**2)
            if gravity_score>gravity_threshold:
                data.append((city1['name'], city2['name'], city1["pop"], city2["pop"], hsr(mi), mult, gravity_score))
    data=pd.DataFrame(data, columns=['City1', 'City2', 'Pop1', 'Pop2', 'Dist', 'Multiplier', 'Gravity Score'])
    data=data.sort_values(by='Gravity Score', ascending=False)
    data.to_csv("output/selected_data.csv", index=False)

if __name__ == "__main__":
    main()
    print("done")