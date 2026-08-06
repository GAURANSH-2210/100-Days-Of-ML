mission_name = "Astra-7"
crew_members = 5

oxygen_per_person = 0.84       # kg/day
water_per_person = 3.2         # litres/day
food_per_person = 2.1          # kg/day

mission_days = 18

oxygen_available = 125.0       # kg
water_available = 475.0        # litres
food_available = 315.0         # kg

emergency_reserve_percent = 12

print("========== ASTRA-7 MISSION REPORT ==========")
print("Original Mission\nMission Duration: ", mission_days, " days\nCrew Members: ", crew_members, sep="")
print("\n")

print("--------- RESOURCE REQUIREMENTS ---------")
total_oxygen_required = oxygen_per_person * crew_members * mission_days
total_water_required = water_per_person * crew_members * mission_days
total_food_required = food_per_person * crew_members * mission_days
print("Oxygen Required: ", total_oxygen_required, " kg", sep="")
print("Water Required: ", total_water_required, " L", sep="")
print("Food Required: ", total_food_required, " kg", sep="")
print("\n")

print("--------- USABLE RESOURCES ---------")
total_oxygen_available = oxygen_available * (1 - emergency_reserve_percent / 100)
total_water_available = water_available * (1 - emergency_reserve_percent / 100)
total_food_available = food_available * (1 - emergency_reserve_percent / 100)
print("Oxygen: ", total_oxygen_available, " kg", sep="")
print("Water: ", total_water_available, " L", sep="")
print("Food: ", total_food_available, " kg", sep="")
print("\n")

print("--------- REMAINING RESOURCES ---------")
remaining_oxygen = total_oxygen_available - total_oxygen_required
remaining_water = total_water_available - total_water_required
remaining_food = total_food_available - total_food_required
print("Oxygen: ", remaining_oxygen, " kg", sep="")
print("Water: ", remaining_water, " L", sep="")
print("Food: ", remaining_food, " kg", sep="")
print("\n")

print("========= MISSION UPDATE ==========")
extra_days=4
print("Mission extended by 4 days.\n")
mission_days += extra_days
print("Mission Duration: ", mission_days, " days", sep="")
print("\n")

print("========= CREW UPDATE ==========")
extra_crew=1
print("Additional Astronaut needed.\n")
crew_members += extra_crew
print("Crew Size: ", crew_members, sep="")
print("\n")

print("========= SURVIVAL ANALYSIS ==========")
oxygen_per_day = oxygen_per_person * crew_members
water_per_day = water_per_person * crew_members
food_per_day = food_per_person * crew_members
print("Need to survive 4 more days.\n")
print("Oxygen supports ", remaining_oxygen // oxygen_per_day, " days", sep="")
print("Water supports ", remaining_water // water_per_day, " days", sep="")
print("Food supports ", remaining_food // food_per_day, " days", sep="")