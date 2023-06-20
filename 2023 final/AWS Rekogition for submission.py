import cv2
import boto3
import pprint
import tempfile
import webbrowser

# AWS Rekognition 설정
client = boto3.client(
    "rekognition",
    aws_access_key_id="AKIA3KD6RYMM7VF7VCHC",
    aws_secret_access_key="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",
    region_name="ap-northeast-2"
)

# S3 설정
s3_client = boto3.client(
    's3',
    aws_access_key_id="AKIA3KD6RYMM7VF7VCHC",
    aws_secret_access_key="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",
    region_name="ap-northeast-2" #서울
)
# 이미지 파일 경로
image_path = r'C:\Users\kcy\Desktop\testing3.jpg'

# 이미지 로드 및 리사이징
# 이미지 -> 제한된 bytes를 초과 -> 크기 조정 소스 추가.
image = cv2.imread(image_path)
resized_image = cv2.resize(image, (800, 600))  # 이미지 크기 조정

# 이미지 로드
image = cv2.imread(image_path)

# 바운딩 박스 그리기
def draw_bounding_box(image, bbox, label):
    height, width, _ = image.shape
    x = int(bbox['Left'] * width)
    y = int(bbox['Top'] * height)
    w = int(bbox['Width'] * width)
    h = int(bbox['Height'] * height)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# 이미지를 Amazon Rekognition으로 전송하여 객체 감지 수행
with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_image:
    cv2.imwrite(temp_image.name, resized_image)

    with open(temp_image.name, 'rb') as image_file:
        response = client.detect_labels(
            Image={'Bytes': image_file.read()},
            MaxLabels=15,
            MinConfidence=20
        )

# 레이블 정보 추출 및 바운딩 박스 그리기
labels = response['Labels']
for label in labels:
    instances = label['Instances']
    for instance in instances:
        bbox = instance['BoundingBox']
        draw_bounding_box(image, bbox, label['Name'])

# 이미지를 임시 파일로 저장
temp_image_path = tempfile.mktemp(suffix='.jpg')
cv2.imwrite(temp_image_path, image)

# S3 버킷 이름과 객체 이름 설정
bucket_name = "choigod"
object_name = "test4.jpg"

# 이미지 업로드 함수
def upload_image_to_s3(image_path, bucket_name, object_name):
    with open(image_path, 'rb') as image_file:
        s3_client.upload_fileobj(image_file, bucket_name, object_name)

# 이미지 업로드
upload_image_to_s3(temp_image_path, bucket_name, object_name)
# 외부 이미지 뷰어로 이미지 열기
webbrowser.open(temp_image_path)

# 결과 출력
pprint.pprint(response)
