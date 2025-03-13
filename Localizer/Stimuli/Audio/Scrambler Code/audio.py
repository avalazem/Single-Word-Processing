import argparse
import pathlib
from typing import TypedDict

import matplotlib.pyplot as plt
import numpy as np
from numpy.random import default_rng
from scipy.fft import fft
from scipy.io import wavfile
from scipy.signal import butter, lfilter


class FilterCoefs(TypedDict):
    A0: np.ndarray
    A11: np.ndarray
    A12: np.ndarray
    A13: np.ndarray
    A14: np.ndarray
    A2: np.ndarray
    B0: np.ndarray
    B1: np.ndarray
    B2: np.ndarray
    gain: np.ndarray


def make_erbfilters(
    fs: float, num_channels: int, lowfreq: int | float, test: bool = False
) -> tuple[FilterCoefs, np.ndarray]:
    r"""
    This function computes the filter coefficients for a bank of
    Gammatone filters.  These filters were defined by Patterson and
    Holdworth for simulating the cochlea.

    The result is returned as an array of filter coefficients.  Each row
    of the filter arrays contains the coefficients for four second order
    filters.  The transfer function for these four filters share the same
    denominator (poles) but have different numerators (zeros).  All of these
    coefficients are assembled into one vector that the ERBFilterBank
    can take apart to implement the filter.

    The filter bank contains "numChannels" channels that extend from
    half the sampling rate (fs) to "lowFreq".

    Note this implementation fixes a problem in the original code by
    computing four separate second order filters.  This avoids a big
    problem with round off errors in cases of very small cfs (100Hz) and
    large sample rates (44kHz).  The problem is caused by roundoff error
    when a number of poles are combined, all very close to the unit
    circle.  Small errors in the eigth order coefficient, are multiplied
    when the eigth root is taken to give the pole location.  These small
    errors lead to poles outside the unit circle and instability.  Thanks
    to Julius Smith for leading me to the proper explanation.

    Execute the following code to evaluate the frequency
    response of a 10 channel filterbank.
        fcoefs = MakeERBFilters(16000,10,100);
        y = ERBFilterBank([1 zeros(1,511)], fcoefs);
        resp = 20*log10(abs(fft(y_prime)));
        freqScale = (0:511)/512*16000;
        semilogx(freqScale(1:255),resp(1:255,:));
        axis([100 16000 -60 0])
        xlabel('Frequency (Hz)'); ylabel('Filter Response (dB)');

    Rewritten by Malcolm Slaney@Interval.  June 11, 1998.
    (c) 1998 Interval Research Corporation
    """

    T = 1 / fs

    # Change the following parameters if you wish to use a different ERB scale.
    EarQ = 9.26449  # Glasberg and Moore Parameters
    minBW = 24.7
    order = 1

    # All of the following expressions are derived in Apple TR #35, "An
    # Efficient Implementation of the Patterson-Holdsworth Cochlear
    # Filter Bank."  See pages 33-34.
    center_freqs = -(EarQ * minBW) + np.exp(
        np.arange(1, num_channels + 1)
        * (-np.log(fs / 2 + EarQ * minBW) + np.log(lowfreq + EarQ * minBW))
        / num_channels
    ) * (fs / 2 + EarQ * minBW)
    ERB = ((center_freqs / EarQ) ** order + minBW**order) ** (1 / order)
    B = 1.019 * 2 * np.pi * ERB

    the_cos = np.cos(2 * center_freqs * np.pi * T)
    the_sin = np.sin(2 * center_freqs * np.pi * T)
    A0 = T
    A2 = 0
    B0 = 1
    B1 = -2 * the_cos * np.exp(-B * T)
    B2 = np.exp(-2 * B * T)

    A11 = -T * (the_cos + np.sqrt(3 + 2**1.5) * the_sin) * np.exp(-B * T)
    A12 = -T * (the_cos - np.sqrt(3 + 2**1.5) * the_sin) * np.exp(-B * T)
    A13 = -T * (the_cos + np.sqrt(3 - 2**1.5) * the_sin) * np.exp(-B * T)
    A14 = -T * (the_cos - np.sqrt(3 - 2**1.5) * the_sin) * np.exp(-B * T)

    the_exp = np.exp(4j * np.pi * center_freqs * T)
    the_other_exp = np.exp(-(B * T) + 2j * np.pi * center_freqs * T)
    gain = np.absolute(
        (-the_exp * T + the_other_exp * T * (the_cos - np.sqrt(3 - 2**1.5) * the_sin))
        * (-the_exp * T + the_other_exp * T * (the_cos + np.sqrt(3 - 2**1.5) * the_sin))
        * (-the_exp * T + the_other_exp * T * (the_cos - np.sqrt(3 + 2**1.5) * the_sin))
        * (-the_exp * T + the_other_exp * T * (the_cos + np.sqrt(3 + 2**1.5) * the_sin))
        / (-np.exp(-2 * B * T) - the_exp + (1 + the_exp) * np.exp(-B * T)) ** 4
    )

    allfilts = np.ones(num_channels)
    filter_coefs = FilterCoefs(
        {
            "A0": A0 * allfilts,
            "A11": A11,
            "A12": A12,
            "A13": A13,
            "A14": A14,
            "A2": A2 * allfilts,
            "B0": B0 * allfilts,
            "B1": B1,
            "B2": B2,
            "gain": gain,
        }
    )

    if test:  # Test Code
        raise NotImplementedError
        # A0 = fcoefs["A0"]
        # A2 = fcoefs["A2"]
        # B0 = fcoefs["B0"]
        # for chan in range(num_channels):
        #     x = np.zeros(2048)
        #     x[0] = 1
        #     y1 = lfilter(
        #         [A0[chan] / gain[chan], A11[chan] / gain[chan], A2[chan] / gain[chan]],
        #         [B0[chan], B1[chan], B2[chan]],
        #         x,
        #     )
        #     y2 = lfilter(
        #         [A0[chan], A12[chan], A2[chan]], [B0[chan], B1[chan], B2[chan]], y1
        #     )
        #     y3 = lfilter(
        #         [A0[chan], A13[chan], A2[chan]], [B0[chan], B1[chan], B2[chan]], y2
        #     )
        #     y4 = lfilter(
        #         [A0[chan], A14[chan], A2[chan]], [B0[chan], B1[chan], B2[chan]], y3
        #     )
        #     plt.semilogx(
        #         np.arange(len(x)) * (fs / len(x)), 20 * np.log10(np.abs(fft(y4)))
        #     )
        #     # cleanfft(y4,fs,'ld')
        #     # % spectrum(y4,2048,0,2048,fs)
        #     # % freqz(y4)
        #     # figure(2)
        #     # plot(y4)
        #     # TODO add show code

    return filter_coefs, center_freqs


def erbfilterbank(
    signal: np.ndarray, filter_coefs: FilterCoefs | None = None, test: bool = False
) -> np.ndarray:
    r"""
    Process an input waveform with a gammatone filter bank.  Design the
    fcoefs parameter, which completely specifies the Gammatone filterbank,
    with the MakeERBFilters function.

    This function takes a single sound vector, and returns an array of filter
    outputs, one output per column.  The filter coefficients are computed for
    you if you do not specify them.  The default Gammatone filter bank assumes
    a 22050Hz sampling rate, and provides 64 filters down to 100Hz.

    Malcolm Slaney @ Interval, June 11, 1998.
    (c) 1998 Interval Research Corporation
    """
    if filter_coefs is None:
        filter_coefs, _ = make_erbfilters(22050, 64, 100)

    A0 = filter_coefs["A0"]
    A11 = filter_coefs["A11"]
    A12 = filter_coefs["A12"]
    A13 = filter_coefs["A13"]
    A14 = filter_coefs["A14"]
    A2 = filter_coefs["A2"]
    B0 = filter_coefs["B0"]
    B1 = filter_coefs["B1"]
    B2 = filter_coefs["B2"]
    gain = filter_coefs["gain"]
    num_channels = len(gain)

    filtered_signal = np.zeros((num_channels, len(signal)))
    for freq_chan in range(num_channels):
        y1 = lfilter(
            [
                A0[freq_chan] / gain[freq_chan],
                A11[freq_chan] / gain[freq_chan],
                A2[freq_chan] / gain[freq_chan],
            ],
            [B0[freq_chan], B1[freq_chan], B2[freq_chan]],
            signal,
        )
        y2 = lfilter(
            [A0[freq_chan], A12[freq_chan], A2[freq_chan]],
            [B0[freq_chan], B1[freq_chan], B2[freq_chan]],
            y1,
        )
        y3 = lfilter(
            [A0[freq_chan], A13[freq_chan], A2[freq_chan]],
            [B0[freq_chan], B1[freq_chan], B2[freq_chan]],
            y2,
        )
        y4 = lfilter(
            [A0[freq_chan], A14[freq_chan], A2[freq_chan]],
            [B0[freq_chan], B1[freq_chan], B2[freq_chan]],
            y3,
        )
        filtered_signal[freq_chan] = y4

    if test:
        raise NotImplementedError
        # fs = 22050
        # plt.semilogx(
        #     np.arange(len(signal)) * (fs / len(signal)),
        #     20 * np.log10(np.abs(fft(output))),
        # )
        # TODO add show code

    return filtered_signal


def erbgram(
    signal, fs=44100, dbthresh=60, lowfreq=100, numchan=64, toplot=False
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    r"""
    `fs` : sampling frequency
    `dbthres` : threshold
    """
    filter_coefs, center_freqs = make_erbfilters(fs, numchan, lowfreq)
    B, A = butter(N=2, Wn=70 * 2 / fs)

    filtered_signal = erbfilterbank(signal, filter_coefs)  # 2D array, (n_chan, len_x)

    y = np.maximum(filtered_signal, 0)
    y = lfilter(B, A, y.transpose(), axis=0)
    y = y.transpose()

    my = np.max(y)
    miny = my / (10 ** (dbthresh / 20))
    y = np.maximum(y, miny)

    if toplot:
        raise NotImplementedError
        # t = np.arange(y.shape[1]) / fs * 1000
        # plt.imshow(20 * np.log10(y))
        # f = np.arange(4, numchan + 1, 4)
        # plt.yticks(f, np.round(center_freqs[f]))
        # plt.xticks(t)
        # plt.xlabel("Time (ms)")
        # plt.ylabel("Centre Frequency (Hz)")
        # TODO add show code
    return y, filtered_signal, center_freqs


def grains(
    signal: np.ndarray,
    fs: int,
    window_length: float,
    max_delay: float,
    filtered_signal: np.ndarray | None = None,
    num_channels: int = 64,
    lowfreq: int = 100,
    seed: int = 42,
    plot: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    r"""
    inputs :
        `x` : signal to process, expected to be (N_samples) or (N_samples, N_audio_channels) for stereo
        `fs` : sampling frequency of signal
        `twin` : time of the grains in ms (time of windows)
        `trand` : time that can be jumbed (time of random)
        `xf` : optional previously computed time-frequency analysis, of size
        `num_channels` : number of frequency channels for the gammatone filterbank, defaults to 64
        `lowfreq` : lowest frequency for the channels
        `seed` : seed to use for grain swapping
        `plot` : whether or not to plot the ERBgram

    outputs :
        `xx` : processed signal
        `xf` : a structure with time-frequency analysis of x

    some values that produce interesting results
    `grains(x,5000,10)`
    `grains(x,2000,10)`
    `grains(x,200,100)`
    """
    rng = default_rng(seed=seed)
    sig_length = len(signal)

    stereo = len(signal.shape) > 1

    if filtered_signal is None:
        if stereo:
            filtered_signal = np.empty([num_channels, sig_length, 2], dtype=np.float32)
            _, filtered_1, _ = erbgram(
                signal[:, 0], fs, 60, lowfreq, num_channels, plot
            )
            _, filtered_2, _ = erbgram(
                signal[:, 1], fs, 60, lowfreq, num_channels, plot
            )
            filtered_signal[:, :, 0] = filtered_1.astype(np.float32)
            filtered_signal[:, :, 1] = filtered_2.astype(np.float32)
        else:
            _, filtered_signal, _ = erbgram(signal, fs, 60, lowfreq, num_channels, plot)
            filtered_signal = filtered_signal.astype(np.float32)

    lwin = round(window_length / 1000 * fs)  # compute window length
    lwin += lwin % 2  # make window lenght a multiple of 2

    win = np.hanning(lwin).astype(np.float32)
    if stereo:
        win = win[:, None]  # for broadcasting in stereo
    num_grains = int(2 * np.ceil(sig_length / lwin) - 1)
    npad = int(np.ceil(max_delay / 1000 * fs) + lwin)

    if stereo:
        processed_signal = np.zeros((sig_length + npad, 2), dtype=np.float32)
    else:
        processed_signal = np.zeros((sig_length + npad), dtype=np.float32)
    for freq_chan in range(num_channels):
        for grain in range(num_grains):
            # create grain
            if grain * lwin // 2 + lwin > sig_length:
                pad = (0, grain * lwin // 2 + lwin - sig_length)
                if stereo:
                    pad = (pad, (0, 0))
                grain_sig = np.pad(filtered_signal[freq_chan, grain * lwin // 2 :], pad)
            else:
                grain_sig = filtered_signal[
                    freq_chan, grain * lwin // 2 : grain * lwin // 2 + lwin
                ]
            grain_sig *= win
            # compute delay
            delayed_start = grain * lwin // 2 + int(
                np.ceil(max_delay * rng.random() / 1000 * fs)
            )
            # add delayed grain
            processed_signal[delayed_start : delayed_start + lwin] += grain_sig

    if np.isnan(processed_signal).any():
        raise RuntimeError("NaN values generated during the computations")

    return processed_signal, filtered_signal


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the .wav file to read or the folder to process",
    )
    parser.add_argument("--window", type=float, default=25, help="Window length, in ms")
    parser.add_argument(
        "--delay", type=float, default=500, help="Max delay time, in ms"
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Seed for the grain random delay"
    )
    args = parser.parse_args()

    input_path = pathlib.Path(args.input)

    if input_path.is_file():

        fs, signal = wavfile.read(input_path)

        processed_signal, _ = grains(
            signal, fs, args.window, args.delay, seed=args.seed
        )

        new_wav_path = input_path.parent / f"{input_path.stem}_scrambled.wav"

        wavfile.write(new_wav_path, fs, processed_signal.astype(np.int16))

    elif input_path.is_dir():

        rng = default_rng(seed=args.seed)
        all_files = list(input_path.glob("**/*.wav"))
        num_files = len(all_files)
        print(
            f"Scrambled 0/{num_files} files       ",
            end="\r",
        )
        for i, wav_path in enumerate(all_files):
            fs, signal = wavfile.read(wav_path)

            processed_signal, _ = grains(
                signal.astype(np.int16),
                fs,
                args.window,
                args.delay,
                seed=rng.integers(1 << 32),
            )

            new_wav_path = wav_path.parent / f"{wav_path.stem}_scrambled.wav"

            wavfile.write(new_wav_path, fs, processed_signal.astype(np.int16))
            print(
                f"Scrambled {i+1}/{num_files} files       ",
                end="\r",
            )

    else:
        raise ValueError("Path is pointing to neither a file nor a directory")
