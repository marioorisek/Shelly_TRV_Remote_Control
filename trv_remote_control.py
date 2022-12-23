from requests import get
from time import sleep

debug = True

trv_profile_numbers_lookup = {"Zimni provoz" : "1", "Zimni provoz nemoc" : "2", "Nepouzito" : "3", "Zimni dovolena" : "4", "Letni provoz" : "5"}

trv_defaults_zimni_provoz = [("192.168.20.15", 18, 13), ("192.168.20.16", 21, 18), ("192.168.20.17", 21, 18), ("192.168.20.19", 21, 16), ("192.168.20.18", 21, 16)]
trv_defaults_zimni_provoz_nemoc = [("192.168.20.15", 21, 13), ("192.168.20.16", 21, 18), ("192.168.20.17", 21, 18), ("192.168.20.19", 21, 16), ("192.168.20.18", 21, 16)]
trv_defaults_zimni_dovolena = [("192.168.20.15", 18, 15), ("192.168.20.16", 18, 15), ("192.168.20.17", 18, 16), ("192.168.20.19", 17, 15), ("192.168.20.18", 17, 15)]
trv_defaults_nepouzito = [("192.168.20.15", 10, 10), ("192.168.20.16", 10, 10), ("192.168.20.17", 10, 10), ("192.168.20.19", 10, 10), ("192.168.20.18", 10, 10)]
trv_defaults_letni_provoz = [("192.168.20.15", 10, 10), ("192.168.20.16", 10, 10), ("192.168.20.17", 10, 10), ("192.168.20.19", 10, 10), ("192.168.20.18", 10, 10)]
trv_profile_names = ["Zimni provoz", "Zimni provoz nemoc", "Nepouzito", "Zimni dovolena", "Letni provoz"]
trv_settings = [trv_defaults_zimni_provoz, trv_defaults_zimni_provoz_nemoc, trv_defaults_nepouzito, trv_defaults_zimni_dovolena, trv_defaults_letni_provoz]
trv_settings = list(zip(trv_profile_names, trv_settings))

day_start_time = "0630"
day_end_time = "2100"
day_of_week = "0123456"

def generate_profile_rules_string(setpoint_cfg_list):
    """Function is expecting list of tuples in following format ("time","day of week","temperature") ex. ("0630","0123456","18")"""
    output_list = []
    for setpoint in setpoint_cfg_list:
        time, day, temp = setpoint
        output_list.append(f"{time}-{day}-{temp}")
    output = ",".join(output_list)
    return output

def generate_trv_config_string(profile_number, profile_name, profile_rules):
    """Generates TRV configuration dict"""
    return {"schedule_profile" : profile_number, "profile_name" : profile_name, "schedule_rules" : profile_rules}

def configure_trv_valve(target_ip, config_string):
    """Uploads valve configuration to given TRV valve"""
    url = f"http://{target_ip}/settings/thermostats/0"
    return get(url=url, params=config_string, timeout=60).text

def configure_all_trvs(trv_settings):
    for profile in trv_settings:
        for target in profile[1]:
            schedule = generate_profile_rules_string([(day_start_time,day_of_week,target[1]),(day_end_time,day_of_week,target[2])])
            profile_number = trv_profile_numbers_lookup[profile[0]]
            profile_name = profile[0]
            target_ip = target[0]
            cfg_string = generate_trv_config_string(profile_number, profile_name, schedule)
            response = configure_trv_valve(target_ip, cfg_string)
            print(target_ip, profile_number, profile_name, schedule, response)
            sleep(2)

def set_trv_profiles():
    trv_ip_list = ["192.168.20.15", "192.168.20.16", "192.168.20.17", "192.168.20.18", "192.168.20.19"]
    trv_profiles = [4, 4, 4, 4, 1]
    cfg = list(zip(trv_ip_list, trv_profiles))
    for target in cfg:
        target_ip, profile_number = target
        response = configure_trv_valve(target_ip, {"schedule_profile" : profile_number})
        if debug:
            print(target_ip, profile_number, response)
