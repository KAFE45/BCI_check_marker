from psychopy import visual, core, event
from pylsl import StreamInfo, StreamOutlet

# Create a stream info for LSL
info = StreamInfo('PsychoPyMarkers', 'Markers', 1, 0, 'int32', 'myuidw43536')
outlet = StreamOutlet(info)

# Function to send triggers via LSL
def send_trigger(trigger_code):
    current_time = core.getTime()  # Get current time
    outlet.push_sample([trigger_code])
    print(f'Trigger {trigger_code} sent at {current_time:.2f} seconds')  # Display message when trigger is sent

# Function to run each task
def run_task(start_trigger_code, end_trigger_code, task_text, duration, flicker_freq=None):
    send_trigger(start_trigger_code)  # Send trigger when starting task
    print(f'Starting task {task_text} with start trigger {start_trigger_code}')  # Display message in console

    task_time = core.Clock()
    task_time.reset()

    while task_time.getTime() < duration:
        # Show stimulus or text
        if flicker_freq:
            period = 1.0 / flicker_freq  # Calculate the period for flickering
            half_period = period / 2

            if task_time.getTime() % period < half_period:
                stim.fillColor = 'white'  # White for flicker
            else:
                stim.fillColor = 'black'  # Black when off
            stim.draw()  # Draw stimulus
        else:
            stim.fillColor = 'black'  # If no flicker, show black only
            stim.draw()

        # Draw task text
        text.text = task_text
        text.draw()

        # Update screen
        win.flip()

        # Check for Escape key to exit
        keys = event.getKeys()
        if 'escape' in keys:
            send_trigger(end_trigger_code)  # Send trigger when ending task
            print(f'Ending task {task_text} with end trigger {end_trigger_code}')  # Display message in console
            win.close()
            core.quit()
        elif 'return' in keys:  # Go to next task when Enter is pressed
            break

    send_trigger(end_trigger_code)  # Send trigger when ending task
    print(f'Ending task {task_text} with end trigger {end_trigger_code}')  # Display message in console

# Define trigger codes
static_image_trigger_start = 1  # Start trigger for static image
static_image_trigger_end = 11  # End trigger for static image

ssvep_5hz_trigger_start = 2  # Start trigger for SSVEP 5 Hz
ssvep_5hz_trigger_end = 12  # End trigger for SSVEP 5 Hz

no_trigger_start = 3  # Start Rest Phase
no_trigger_end = 13  # End Rest Phase

ssvep_7hz_trigger_start = 4  # Start trigger for SSVEP 7 Hz
ssvep_7hz_trigger_end = 14  # End trigger for SSVEP 7 Hz

end_trigger = 99  # Trigger for ending the experiment

# Define durations
duration_per_phase = 30  # Duration of each activity (seconds)
ready_duration = 7  # Duration for "Ready go....." message (seconds)

# Window settings
full_screen = True  # Set to True for fullscreen

# Size of flickering stimulus (pixels)
stimulus_size = [400, 400]  # Size of flickering stimulus

# Create window
win = visual.Window(color='black', units='pix', fullscr=full_screen)

# Create stimulus and text
stim = visual.Rect(win, width=stimulus_size[0], height=stimulus_size[1], fillColor='black', pos=(0, 0))
text = visual.TextStim(win, text='', color='white', pos=(0, 0), height=30, alignHoriz='center', alignVert='center')

# Create pre-message
pre_message = visual.TextStim(win, text='Ready go.....', color='white', height=80, alignHoriz='center', alignVert='center')

# Show pre-message
pre_message.draw()
win.flip()

# Start timer for "Ready go..."
ready_time = core.Clock()
ready_time.reset()

# Check for keypress during "Ready go..."
while ready_time.getTime() < ready_duration:
    keys = event.getKeys()
    if 'return' in keys:  # Skip message when Enter is pressed
        break
    elif 'escape' in keys:  # Exit experiment when Escape is pressed
        win.close()
        core.quit()

# Start tasks in order
# Task 1: Static Image (or message)
#run_task(static_image_trigger_start, static_image_trigger_end, "Static Image", duration_per_phase)

# Task 2: Rest (no stimulation)
run_task(no_trigger_start, no_trigger_end, "Rest Phase", duration_per_phase)

# Task 3: SSVEP 5 Hz
run_task(ssvep_5hz_trigger_start, ssvep_5hz_trigger_end, "5 Hz Stimulation", duration_per_phase, flicker_freq=5)

# Task 4: Rest (no stimulation)
run_task(no_trigger_start, no_trigger_end, "Rest Phase", duration_per_phase)

# Task 5: SSVEP 7 Hz
run_task(ssvep_7hz_trigger_start, ssvep_7hz_trigger_end, "7 Hz Stimulation", duration_per_phase, flicker_freq=7)

# Task 6: Rest (no stimulation)
run_task(no_trigger_start, no_trigger_end, "Rest Phase", duration_per_phase)

# Task 7: Ending (end)
run_task(static_image_trigger_start, static_image_trigger_end, "Ending", duration_per_phase)

# Close window
win.close()
core.quit()
