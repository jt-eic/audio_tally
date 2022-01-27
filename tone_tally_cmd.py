#!/usr/bin/env python3
"""From working version that plotted line with matplotlib,
now making it only run in command line; AND auto start?

Matplotlib and NumPy *still* have to be installed.
updated 2/19/2021
"""

import argparse
import queue
import sys
##from LED_GPIS import led_on, led_off

# from matplotlib.animation import FuncAnimation
# import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)



def liton(pin):
    GPIO.output(pin, GPIO.HIGH)
    return GPIO.input(pin)

def litoff(pin):
    GPIO.output(pin, GPIO.LOW)
    return GPIO.input(pin)
    

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument(
    '-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument(
    '-n', '--downsample', type=int, default=10, metavar='N',
    help='display every Nth sample (default: %(default)s)')
args = parser.parse_args(remaining)
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1
q = queue.Queue()


def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::args.downsample, mapping])


def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        # print('the data? ', data, end='\n')
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data

        # this area, use plotdata to determine if GPI goes on or what
        themax = plotdata.max()
        pin = None

        # state of each tally to start:
        cam4 = 22
        cam7 = 25
        t4 = 0
        t7 = 0
        
        if themax > .90:
            t4 = liton(cam4)
            t7 = litoff(cam7)
            print('cam 4 on')
            
        elif themax > .20:
            t7 = liton(cam7)
            t4 = litoff(cam4)
            print('cam 7 on')
            
        elif themax < .10:
            litoff(cam7)
            litoff(cam4)
            t7 = 0
            t4 = 0
            print('all off')

    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines
    

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = device_info['default_samplerate']

    length = int(args.window * args.samplerate / (1000 * args.downsample))
    plotdata = np.zeros((length, len(args.channels)))

##    fig, ax = plt.subplots()
##    lines = ax.plot(plotdata)
##    if len(args.channels) > 1:
##        ax.legend(['channel {}'.format(c) for c in args.channels],
##                  loc='lower left', ncol=len(args.channels))
##    ax.axis((0, len(plotdata), -1, 1))
##    ax.set_yticks([0])
##    ax.yaxis.grid(True)
##    ax.tick_params(bottom=False, top=False, labelbottom=False,
##                   right=False, left=False, labelleft=False)
##    fig.tight_layout(pad=0)
##
    stream = sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback)
##    ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)
    with stream:
        # plt.show()
        print('we have a stream, now instead of plot')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
    print('did we hit the exit?')

GPIO.cleanup()
