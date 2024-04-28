import rosbag
import csv
import argparse
from speech_to_text.msg import Transcript
from std_msgs.msg import String, Int32, Bool
from perceptions_analyzer.msg import DetectedObjects, IdentifiedPerson
from talk.msg import Text, Done, Statistics
from hbba_lite.msg import StrategyState


parser = argparse.ArgumentParser(description="Process bag files and log data to CSV files.")
parser.add_argument('bag_file_path', type=str, help='The path to the rosbag file')
parser.add_argument('csv_output_path_1', type=str, help='Output CSV file path for first set of logs')
parser.add_argument('csv_output_path_2', type=str, help='Output CSV file path for second set of logs')
parser.add_argument('csv_output_path_3', type=str, help='Output CSV file path for third set of logs')
args = parser.parse_args()

def extract_data(msg, msg_type):
    if msg_type == String:
        return [msg.data]
    elif msg_type == Int32:
        return [msg.data]
    elif msg_type == Transcript:
        return [msg.text, msg.is_final]
    elif msg_type == DetectedObjects:
        return [msg.object_name, msg.formatted_detection_time]
    elif msg_type == IdentifiedPerson:
        return [msg.person_name, msg.formatted_detection_time]
    elif msg_type == Text:
        return [msg.text]
    elif msg_type == Done:
        return [msg.ok]
    elif msg_type == StrategyState: 
        return [msg.desire_type_name, msg.strategy_type_name, msg.enabled]
    elif msg_type == Statistics:
        return [msg.header.stamp.to_sec(), msg.text, msg.processing_time_s, msg.total_samples_count]
    else:
        return []

bag = rosbag.Bag(args.bag_file_path)

with open(args.csv_output_path_1, 'w') as csvfile:
    filewriter = csv.writer(csvfile)
    for topic, msg, t in bag.read_messages():
        data = extract_data(msg, globals()[topic.split('/')[-1]])
        if data:
            filewriter.writerow(data + [t.to_sec()])

with open(args.csv_output_path_2, 'w') as csvfile:
    filewriter = csv.writer(csvfile)
    for topic, msg, t in bag.read_messages():
        if topic in ['/hbba_strategy_state_log', '/speech_to_text/transcript']:
            data = extract_data(msg, globals()[topic.split('/')[-1]])
            filewriter.writerow(data + [t.to_sec()])

with open(args.csv_output_path_3, 'w') as csvfile:
    filewriter = csv.writer(csvfile)
    for topic, msg, t in bag.read_messages():
        if topic in ['/hbba_strategy_state_log', '/talk/statistics']:
            data = extract_data(msg, globals()[topic.split('/')[-1]])
            filewriter.writerow(data + [t.to_sec()])

bag.close()
