import requests
import json

# ENVs
from dotenv import load_dotenv
config = load_dotenv(".env")
import os

# credentials
unifi = os.getenv("UNIFI_CONTROLLER")
username = os.getenv("UNIFI_USERNAME")
password = os.getenv("UNIFI_PASSWORD")
wifi_network = os.getenv("WIFI_NETWORK_ID")
site = os.getenv("SITE")

class Unifi():
    # Disable HTTPS verification because of Self-signed cert
    requests.packages.urllib3.disable_warnings()

    # Login duh
    def auth():
        try:
            payload = json.dumps({"username": username, "password": password})
            r = requests.post(f"{unifi}/api/login", verify=False, data=payload)

            if r.json()["meta"]["rc"] != "ok":
                raise Exception("request to unifi controller failed")

            session_token = r.cookies["unifises"]
            anti_forgery = r.cookies["csrf_token"]

            return session_token, anti_forgery

        except Exception as e:
            print("ERROR:", e)

    # Get the current state of the wireless network
    def get_wifi_config(session_token, anti_forgery):
        try:
            headers = {'accept': 'application/json', 'Content-Type': 'application/json;charset=UTF-8', 'X-Csrf-Token': anti_forgery}
            
            jar = requests.cookies.RequestsCookieJar()
            jar.set('unifises', session_token)
            jar.set('csrf_token', anti_forgery)
            
            r = requests.get(f"{unifi}/api/s/{site}/rest/wlanconf/{wifi_network}", verify=False, headers=headers, cookies=jar)

            if r.json()["meta"]["rc"] != "ok":
                raise Exception("request to unifi controller failed")

            return r.json()["data"][0]

        except Exception as e:
            print("ERROR:", e)

    # Sets the password and create the right JSON body
    def create_set_wifi_config_payload (currentWifi, new_password):
        return json.dumps({
            "ap_group_ids": currentWifi["ap_group_ids"],
            "enabled": currentWifi["enabled"],
            "fast_roaming_enabled": currentWifi["fast_roaming_enabled"],
            "hide_ssid": currentWifi["hide_ssid"],
            "name": currentWifi["name"],
            "networkconf_id": currentWifi["networkconf_id"],
            "pmf_mode": currentWifi["pmf_mode"],
            "usergroup_id": currentWifi["usergroup_id"],
            "wlan_bands": currentWifi["wlan_bands"],
            "wpa_enc": currentWifi["wpa_enc"],
            "x_passphrase": new_password,
            "wpa3_support": currentWifi["wpa3_support"],
            "wpa3_transition": currentWifi["wpa3_transition"],
            "wpa3_fast_roaming": currentWifi["wpa3_fast_roaming"],
            "wpa3_enhanced_192": currentWifi["wpa3_enhanced_192"],
            "group_rekey": currentWifi["group_rekey"],
            "uapsd_enabled": currentWifi["uapsd_enabled"],
            "mcastenhance_enabled": currentWifi["mcastenhance_enabled"],
            "no2ghz_oui": currentWifi["no2ghz_oui"],
            "bss_transition": currentWifi["bss_transition"],
            "proxy_arp": currentWifi["proxy_arp"],
            "l2_isolation": currentWifi["l2_isolation"],
            "b_supported": currentWifi["b_supported"],
            "optimize_iot_wifi_connectivity": currentWifi["optimize_iot_wifi_connectivity"],
            "dtim_mode": currentWifi["dtim_mode"],
            "minrate_ng_enabled": currentWifi["minrate_ng_enabled"],
            "minrate_ng_data_rate_kbps": currentWifi["minrate_ng_data_rate_kbps"],
            "minrate_ng_advertising_rates": currentWifi["minrate_ng_advertising_rates"],
            "minrate_na_enabled": currentWifi["minrate_na_enabled"],
            "minrate_na_data_rate_kbps": currentWifi["minrate_na_data_rate_kbps"],
            "minrate_na_advertising_rates": currentWifi["minrate_na_advertising_rates"],
            "mac_filter_enabled": currentWifi["mac_filter_enabled"],
            "mac_filter_policy": currentWifi["mac_filter_policy"],
            "mac_filter_list": currentWifi["mac_filter_list"],
            "radius_mac_auth_enabled": currentWifi["radius_mac_auth_enabled"],
            "radius_macacl_format": currentWifi["radius_macacl_format"],
            "_id": currentWifi["_id"],
            "security": currentWifi["security"],
            "wpa_mode": currentWifi["wpa_mode"],
            "bc_filter_enabled": currentWifi["bc_filter_enabled"],
            "bc_filter_list": currentWifi["bc_filter_list"],
            "auth_cache": currentWifi["auth_cache"],
            "schedule_reversed": currentWifi["schedule_reversed"],
            "radius_das_enabled": currentWifi["radius_das_enabled"],
            "schedule": currentWifi["schedule"],
            "x_iapp_key": currentWifi["x_iapp_key"],
            "is_guest": currentWifi["is_guest"],
            "schedule_enabled": currentWifi["schedule_enabled"],
            "iapp_enabled": currentWifi["iapp_enabled"],
            "pmf_cipher": currentWifi["pmf_cipher"],
            "minrate_ng_mgmt_rate_kbps": 6000,
            "minrate_ng_beacon_rate_kbps": 6000,
            "minrate_na_mgmt_rate_kbps": 6000,
            "minrate_na_beacon_rate_kbps": 6000
        })

    # Makes the request to set the password
    def set_wifi_config(session_token, anti_forgery, config):
        try:
            headers = {'accept': 'application/json', 'Content-Type': 'application/json;charset=UTF-8', 'X-Csrf-Token': anti_forgery}
            
            jar = requests.cookies.RequestsCookieJar()
            jar.set('unifises', session_token)
            jar.set('csrf_token', anti_forgery)
            
            r = requests.put(f"{unifi}/api/s/{site}/rest/wlanconf/{wifi_network}", verify=False, headers=headers, cookies=jar, data=config)

            if r.json()["meta"]["rc"] != "ok":
                raise Exception("request to unifi controller failed")

        except Exception as e:
            print("ERROR:", e)