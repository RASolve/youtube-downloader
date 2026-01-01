import streamlit as st
import yt_dlp
import os
import shutil

st.title("📺 나만의 유튜브 다운로더")
st.write("링크만 넣으면 서버에서 받아 내 컴퓨터로 다운로드합니다.")

# 입력창
url = st.text_input("유튜브 링크(또는 재생목록)를 입력하세요:")

# 다운로드 버튼
if st.button("다운로드 시작"):
    if not url:
        st.error("링크를 입력해주세요!")
    else:
        status_text = st.empty()
        status_text.info("🚀 서버에서 영상을 분석하고 다운로드 중입니다...")
        
        # 임시 저장 폴더 설정
        download_path = "downloads"
        if os.path.exists(download_path):
            shutil.rmtree(download_path)
        os.makedirs(download_path)
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': f'{download_path}/%(playlist_index)s - %(title)s.%(ext)s',
            'noplaylist': False,
            'quiet': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            status_text.success("✅ 서버 다운로드 완료! 압축 중...")
            
            # 압축하기
            shutil.make_archive("youtube_files", 'zip', download_path)
            
            # 다운로드 버튼 생성
            with open("youtube_files.zip", "rb") as file:
                btn = st.download_button(
                    label="📥 내 컴퓨터로 파일 저장하기 (클릭)",
                    data=file,
                    file_name="youtube_videos.zip",
                    mime="application/zip"
                )
            status_text.success("아래 버튼을 눌러 파일을 저장하세요!")
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")