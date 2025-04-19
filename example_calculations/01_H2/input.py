from BSEGradients import parameters, run_excited_state_geoopt

params = parameters()

params.directory_BSE_calcs         = "./BSE"
params.excited_state_to_optimize   = 1

run_excited_state_geoopt(params)
