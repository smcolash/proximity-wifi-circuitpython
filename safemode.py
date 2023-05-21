import microcontroller
import supervisor

supervisor.autoreload = False

if supervisor.runtime.safe_mode_reason == supervisor.SafeModeReason.BROWNOUT:
    microcontroller.reset()
