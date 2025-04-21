v4l2-ctl -d /dev/video2 -c focus_automatic_continuous=0
v4l2-ctl -d /dev/video2 -c auto_exposure=1
v4l2-ctl -d /dev/video2 -c white_balance_automatic=0

v4l2-ctl -d /dev/video2 -c sharpness=10
v4l2-ctl -d /dev/video2 -c tilt_absolute=$(bc <<<"3600 * 2")
v4l2-ctl -d /dev/video2 -c focus_absolute=26
v4l2-ctl -d /dev/video2 -c brightness=70
v4l2-ctl -d /dev/video2 -c exposure_time_absolute=20
v4l2-ctl -d /dev/video2 -c white_balance_temperature=2500
v4l2-ctl -d /dev/video2 -c zoom_absolute=115
