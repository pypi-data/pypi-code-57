#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DeadCanadian
# 	named a few things and set the types of a few
# revision: 3		author: Lord Zedd
# 	I don't always add revisions, but when I do it's because I spend hours making these giant enums.
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

goof_game_engine_setting_setting_category = (
    "none",
    "global_respawn_options",
    "global_social_options",
    "global_map_overrides",
    "global_base_traits_main",
    "global_base_traits_health",
    "global_base_traits_weapons",
    "global_base_traits_movement",
    "global_base_traits_sensors",
    "global_base_traits_appearance",
    "unknown_0",
    "global_respawn_traits_main",
    "global_respawn_traits_health",
    "global_respawn_traits_weapons",
    "global_respawn_traits_movement",
    "global_respawn_traits_sensors",
    "global_respawn_traits_appearance",
    "unknown_1",
    "global_powerups_red_traits_main",
    "global_powerups_red_traits_health",
    "global_powerups_red_traits_weapons",
    "global_powerups_red_traits_movement",
    "global_powerups_red_traits_sensors",
    "global_powerups_red_traits_appearance",
    "unknown_2",
    "global_powerups_blue_traits_main",
    "global_powerups_blue_traits_health",
    "global_powerups_blue_traits_weapons",
    "global_powerups_blue_traits_movement",
    "global_powerups_blue_traits_sensors",
    "global_powerups_blue_traits_appearance",
    "unknown_3",
    "global_powerups_yellow_traits_main",
    "global_powerups_yellow_traits_health",
    "global_powerups_yellow_traits_weapons",
    "global_powerups_yellow_traits_movement",
    "global_powerups_yellow_traits_sensors",
    "global_powerups_yellow_traits_appearance",
    "unknown_4",
    "unknown_5",
    "slayer_leader_traits_main",
    "slayer_leader_traits_health",
    "slayer_leader_traits_weapons",
    "slayer_leader_traits_movement",
    "slayer_leader_traits_sensors",
    "slayer_leader_traits_appearance",
    "unknown_6",
    "oddball_carrier_traits_main",
    "oddball_carrier_traits_health",
    "oddball_carrier_traits_weapons",
    "oddball_carrier_traits_movement",
    "oddball_carrier_traits_sensors",
    "oddball_carrier_traits_appearance",
    "unknown_7",
    "assault_carrier_traits_main",
    "assault_carrier_traits_health",
    "assault_carrier_traits_weapons",
    "assault_carrier_traits_movement",
    "assault_carrier_traits_sensors",
    "assault_carrier_traits_appearance",
    "unknown_8",
    "ctf_carrier_traits_main",
    "ctf_carrier_traits_health",
    "ctf_carrier_traits_weapons",
    "ctf_carrier_traits_movement",
    "ctf_carrier_traits_sensors",
    "ctf_carrier_traits_appearance",
    "unknown_9",
    "juggernaut_juggy_traits_main",
    "juggernaut_juggy_traits_health",
    "juggernaut_juggy_traits_weapons",
    "juggernaut_juggy_traits_movement",
    "juggernaut_juggy_traits_sensors",
    "juggernaut_juggy_traits_appearance",
    "unknown_10",
    "koth_hill_traits_main",
    "koth_hill_traits_health",
    "koth_hill_traits_weapons",
    "koth_hill_traits_movement",
    "koth_hill_traits_sensors",
    "koth_hill_traits_appearance",
    "unknown_11",
    "infection_zombie_traits_main",
    "infection_zombie_traits_health",
    "infection_zombie_traits_weapons",
    "infection_zombie_traits_movement",
    "infection_zombie_traits_sensors",
    "infection_zombie_traits_appearance",
    "unknown_12",
    "infection_alpha_zombie_traits_main",
    "infection_alpha_zombie_traits_health",
    "infection_alpha_zombie_traits_weapons",
    "infection_alpha_zombie_traits_movement",
    "infection_alpha_zombie_traits_sensors",
    "infection_alpha_zombie_traits_appearance",
    "unknown_13",
    "infection_safe_haven_traits_main",
    "infection_safe_haven_traits_health",
    "infection_safe_haven_traits_weapons",
    "infection_safe_haven_traits_movement",
    "infection_safe_haven_traits_sensors",
    "infection_safe_haven_traits_appearance",
    "unknown_14",
    "infection_last_man_traits_main",
    "infection_last_man_traits_health",
    "infection_last_man_traits_weapons",
    "infection_last_man_traits_movement",
    "infection_last_man_traits_sensors",
    "infection_last_man_traits_appearance",
    "unknown_15",
    "unknown_unknown_traits_main",
    "unknown_unknown_traits_health",
    "unknown_unknown_traits_weapons",
    "unknown_unknown_traits_movement",
    "unknown_unknown_traits_sensors",
    "unknown_unknown_traits_appearance",
    "unknown_16",
    "territories_defender_traits_main",
    "territories_defender_traits_health",
    "territories_defender_traits_weapons",
    "territories_defender_traits_movement",
    "territories_defender_traits_sensors",
    "territories_defender_traits_appearance",
    "unknown_17",
    "territories_attacker_traits_main",
    "territories_attacker_traits_health",
    "territories_attacker_traits_weapons",
    "territories_attacker_traits_movement",
    "territories_attacker_traits_sensors",
    "territories_attacker_traits_appearance",
    "unknown_18",
    "vip_team_traits_main",
    "vip_team_traits_health",
    "vip_team_traits_weapons",
    "vip_team_traits_movement",
    "vip_team_traits_sensors",
    "vip_team_traits_appearance",
    "unknown_19",
    "vip_influence_traits_main",
    "vip_influence_traits_health",
    "vip_influence_traits_weapons",
    "vip_influence_traits_movement",
    "vip_influence_traits_sensors",
    "vip_influence_traits_appearance",
    "unknown_20",
    "vip_vip_traits_main",
    "vip_vip_traits_health",
    "vip_vip_traits_weapons",
    "vip_vip_traits_movement",
    "vip_vip_traits_sensors",
    "vip_vip_traits_appearance",
    "unknown_21",
    "editor_editor_traits_main",
    "editor_editor_traits_health",
    "editor_editor_traits_weapons",
    "editor_editor_traits_movement",
    "editor_editor_traits_sensors",
    "editor_editor_traits_appearance",
    "unknown_22",
    "ctf_top",
    "slayer_top",
    "oddball_top",
    "koth_top",
    "editor_top",
    "juggernaut_top",
    "territories_top",
    "assault_top",
    "infection_top",
    "vip_top",
    "unknown_23",
    "global_powerups",
    "global_respawn_advanced",
    "global_respawn_modifiers",
    "slayer_main",
    "unknown_24",
    "slayer_scoring",
    "oddball_main",
    "oddball_scoring",
    "assault_main",
    "assault_scoring",
    "ctf_main",
    "ctf_scoring",
    "juggernaut_main",
    "juggernaut_scoring",
    "koth_main",
    "koth_scoring",
    "infection_main",
    "infection_advanced",
    "infection_scoring",
    "unknown_25",
    "unknown_26",
    "unknown_27",
    "unknown_28",
    "unknown_29",
    "unknown_30",
    "unknown_31",
    "unknown_32",
    "unknown_33",
    "unknown_34",
    "unknown_35",
    "unknown_36",
    "vip_main",
    "vip_scoring",
    "territories_main",
    "territories_scoring",
    "templates_traits_main",
    "templates_traits_health",
    "templates_traits_weapons",
    "templates_traits_movement",
    "templates_traits_sensors",
    "templates_traits_appearance",
    "templates_dynamic_traits_main",
    "templates_dynamic_traits_health",
    "templates_dynamic_traits_weapons",
    "templates_dynamic_traits_movement",
    "templates_dynamic_traits_sensors",
    "templates_dynamic_traits_appearance",
    )


goof_game_engine_setting_option = Struct("option",
    h3_dependency("explicit_submenu"),
    h3_dependency("template_based_submenu"),
    SEnum32("submenu_setting_category", *goof_game_engine_setting_setting_category),
    h3_string_id("submenu_name"),
    h3_string_id("submenu_description"),
    h3_dependency("value_pairs"),
    ENDIAN=">", SIZE=60
    )


goof_game_engine_setting = Struct("game_engine_setting",
    h3_string_id("name"),
    SEnum32("setting_category", *goof_game_engine_setting_setting_category),
    h3_reflexive("options", goof_game_engine_setting_option),
    ENDIAN=">", SIZE=20
    )


goof_body = Struct("tagdata",
    SInt32("unknown", VISIBLE=False),
    h3_reflexive("game_engine_settings", goof_game_engine_setting),
    ENDIAN=">", SIZE=16
    )


def get():
    return goof_def

goof_def = TagDef("goof",
    h3_blam_header('goof'),
    goof_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["goof"], endian=">", tag_cls=H3Tag
    )
