# GLOBAL COMBAT VARIABLE TO STORE WHO HAD ALREADY ATTACKED INSIDE THE CURRENT ROUND

global took_action
took_action = {
	'Hero': False,
	'enemy': False
}


def reset_rounds():
	global took_action
	took_action = {
		'Hero': False,
		'enemy': False
	}
