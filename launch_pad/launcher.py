from launch_pad.experiment_x import Experiment


class Launcher:
    def __init__(self, optimal_model, ongoing_trials):
        self.optimal_model = optimal_model
        self.ongoing_trials = ongoing_trials
    def launch_c(self):

        for trial_id, trial in self.ongoing_trials.trials.items():
            experiment = Experiment(trial['hp_values'], self.optimal_model)
            metrics = experiment.run()

            self.ongoing_trials.update_metrics(trial_id, metrics)

