import os
import requests
from supabase import create_client, Client

# 데스크톱 앱에서는 Streamlit(st)을 사용할 수 없으므로 전역 변수로 캐싱 역할을 대신합니다.
_supabase_client = None

def get_supabase_client() -> Client:
    global _supabase_client
    if _supabase_client is None:
        # 데스크톱(.exe) 배포용이므로 API 키를 직접 명시합니다. (RLS 정책으로 보안 유지)
        supabase_url = "https://gkzbiacodysnrzbpvavm.supabase.co"
        # 주의: 아래 키는 반드시 'eyJ...' 로 시작하는 긴 anon 키여야 합니다!
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdremJpYWNvZHlzbnJ6YnB2YXZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM1NzE2MTgsImV4cCI6MjA4OTE0NzYxOH0.Lv5uVeNZOyo21tgyl2jjGcESoLl_iQTJYp4jdCwuYDU"
        
        _supabase_client = create_client(supabase_url, supabase_key)
    return _supabase_client

supabase = get_supabase_client()

def get_location_data():
    """사용자의 IP를 기반으로 익명화된 위치 정보를 가져옵니다."""
    try:
        response = requests.get('http://ip-api.com/json/?fields=status,country,regionName,city,lat,lon', timeout=3)
        data = response.json()
        if data['status'] == 'success':
            return {
                'country': data['country'],
                'region': data['regionName'],
                'city': data['city'],
                'lat': data['lat'],
                'lon': data['lon']
            }
    except Exception as e:
        pass # 데스크톱 앱이므로 에러 출력은 생략합니다.
    return None

def log_app_usage(app_name: str, action: str, details: dict = None):
    """Supabase에 사용 로그를 기록합니다."""
    try:
        location = get_location_data()
        log_data = {
            'app_name': app_name,
            'action': action,
            'details': details or {},
        }
        if location:
            log_data.update({
                'country': location['country'],
                'region': location['region'],
                'city': location['city'],
                'lat': location['lat'],
                'lon': location['lon']
            })
        supabase.table('usage_logs').insert(log_data).execute()
    except Exception as e:
        # 사용자 경험을 위해 에러는 출력만 하고 프로그램은 계속 진행시킵니다.
        print(f"로그 기록 실패: {e}")