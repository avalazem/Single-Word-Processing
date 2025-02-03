import numpy as np

def assign_jitter_durations(n_stimuli, mean_soa=5, step=0.5, n_durations=5):
    # Generate evenly spaced duration values
    durations = [mean_soa - step * (i - (n_durations - 1) / 2) for i in range(n_durations)]

    # Compute number of times each duration should be assigned
    base_repeats = n_stimuli // n_durations  # Even distribution
    remainder = n_stimuli % n_durations  # Leftover stimuli

    # Create the duration list
    assigned_durations = durations * base_repeats + [mean_soa] * remainder  # Add mean for remainder cases

    # Shuffle for randomness
    np.random.shuffle(assigned_durations)

    # Check sum (use np.isclose to avoid floating-point errors)
    assert np.isclose(sum(assigned_durations), n_stimuli * mean_soa, atol=1e-6), \
        "Sum of durations does not match the total required duration"

    return assigned_durations

# Example usage:
stimuli_count = 96
durations = assign_jitter_durations(stimuli_count)
print(durations)
print("Mean:", sum(durations) / len(durations))  # Should be 5
