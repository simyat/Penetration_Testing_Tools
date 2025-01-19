#!/bin/bash

# 설정
user_file="user.txt" # 사용자 목록 파일 경로
host="172.31.251.249" # 호스트 주소
password="password" # 패스워드
ssh_key_path="$HOME/.ssh/id_rsa"  # SSH 키 경로
port="22" # 포트 번호
max_attempts=5 # 최대 접속 시도 횟수

# 사용법 함수
usage() {
    echo "사용법: $0 [-k|--key] [-p|--password]"
    echo "  -k, --key      : SSH 키를 사용하여 접속"
    echo "  -p, --password : 패스워드를 사용하여 접속"
    exit 1
}

# 인자 파싱
use_key=false
use_password=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -k|--key)
            use_key=true
            shift
            ;;
        -p|--password)
            use_password=true
            shift
            ;;
        *)
            usage
            ;;
    esac
done

# 접속 방식이 지정되지 않은 경우 사용법 출력
if [[ $use_key == false && $use_password == false ]]; then
    usage
fi

# user.txt 파일 존재 확인
if [[ ! -f "$user_file" ]]; then
    echo "Error: $user_file 파일을 찾을 수 없습니다."
    exit 1
fi

# SSH 키 사용 시 키 파일 존재 확인
if [[ $use_key == true && ! -f "$ssh_key_path" ]]; then
    echo "Error: SSH 키 파일($ssh_key_path)을 찾을 수 없습니다."
    exit 1
fi

attempt=0

# user.txt 파일의 ID를 한 줄씩 읽어서 SSH 접속 시도
while IFS= read -r user; do
    attempt=$((attempt + 1))
    echo "[$attempt] SSH 접속 시도: $user@$host"

    if [[ $use_key == true ]]; then
        # SSH 키를 사용한 접속
        ssh -i "$ssh_key_path" -o StrictHostKeyChecking=no -p "$port" "$user@$host" exit
    fi

    if [[ $use_password == true ]]; then
        # 패스워드를 사용한 접속
        sshpass -p "$password" ssh -o StrictHostKeyChecking=no -p "$port" "$user@$host" exit
    fi

    # SSH 명령의 종료 상태 코드 확인
    if [[ $? -eq 0 ]]; then
        echo "접속 성공: $user@$host"
        break
    else
        echo "접속 실패: $user@$host"
    fi

    # 최대 접속 횟수 초과 시 종료
    if [[ $attempt -ge $max_attempts ]]; then
        echo "최대 접속 시도 횟수($max_attempts)에 도달했습니다."
        break
    fi
done < "$user_file"

echo "SSH 접속 시도가 완료되었습니다." 