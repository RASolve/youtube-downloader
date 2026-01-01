import streamlit as st
import yt_dlp
import os
import shutil

st.title("📺 나만의 유튜브 다운로더 (우회 버전)")
st.write("403 에러 방지 코드가 적용되었습니다.")

url = st.text_input("유튜브 링크(또는 재생목록)를 입력하세요:")

if st.button("다운로드 시작"):
    if not url:
        st.error("링크를 입력해주세요!")
    else:
        status_text = st.empty()
        status_text.info("🚀 보안 우회 시도 및 다운로드 중...")
        
        download_path = "downloads"
        if os.path.exists(download_path):
            shutil.rmtree(download_path)
        os.makedirs(download_path)
        
        # [핵심] 브라우저처럼 보이게 하는 설정
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': f'{download_path}/%(playlist_index)s - %(title)s.%(ext)s',
            'noplaylist': False,
            'quiet': True,
            # 403 에러 방지용 헤더 추가
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.youtube.com/',
            },
            # 지리적 제한 우회 시도
            'geo_bypass': True,
            # 재생목록 오류 무시
            'ignoreerrors': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # 파일이 실제로 받아졌는지 확인
            if not os.listdir(download_path):
                st.error("❌ 유튜브가 서버 IP를 완전히 차단했습니다. (파일 없음)")
                st.warning("💡 해결책: 웹사이트 방식 대신 '내 컴퓨터'에서 파이썬을 실행해야 합니다.")
            else:
                status_text.success("✅ 다운로드 성공! 압축 중...")
                shutil.make_archive("youtube_files", 'zip', download_path)
                
                with open("youtube_files.zip", "rb") as file:
                    btn = st.download_button(
                        label="📥 파일 저장하기",
                        data=file,
                        file_name="youtube_videos.zip",
                        mime="application/zip"
                    )
                status_text.success("버튼을 눌러 저장하세요!")
            
        except Exception as e:
            st.error(f"오류 발생: {e}")
