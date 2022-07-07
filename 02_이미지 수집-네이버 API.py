# pip install aiofiles==0.7.0
# from config import get_secret
import os
import time
import aiohttp
import asyncio
import pyautogui
import aiofiles
from conf import get_secret

class GetNaverImage:
    def __init__(self):
        self.headers = {
            'X-Naver-Client-Id' : get_secret('NAVER_API_ID'),
            'X-Naver-Client-Secret' : get_secret('NAVER_API_SECRET')
        }

        # Base url
        self.base_url = f'https://openapi.naver.com/v1/search/image'

        # Keword
        self.keword = self.input_keword()


    async def run(self):
        start = time.time()

        urls = [self.base_url + f'?query={self.keword}&display=20&start={1 + page * 20}' for page in range(10)]

        # Session Instance Create
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.fetch(session, url) for url in urls])

        end = time.time()

        print(end - start)

    async def fetch(self,session,url: str)-> None:
        async with session.get(url,headers=self.headers) as response:
            # response 데이터 json으로 형변환
            result = await response.json()

            items = result['items']

            images = [item['link'] for item in items]

            await asyncio.gather(*[self.img_downloader(session, img) for img in images])


    async def img_downloader(self,session,img):
        # 이미지 파일 저장경로
        img_save_path = os.path.abspath('images')

        # 현재 경로에 images 폴더 없는 경우 새로 생성
        if not os.path.exists(img_save_path):
            os.mkdir(img_save_path)

        # 이미지 파일 이름 지정
        img_name = img.split('/')[-1].split('?')[0].replace('.jpg','')

        # 이미지 다운로드
        async with session.get(img) as response:
            if response.ok:
                async with aiofiles.open(f'{img_save_path}/{img_name}', mode='wb') as file:
                    img_data = await response.read()
                    await file.write(img_data)

    # 검색어 입력 메서드
    def input_keword(self)-> str:
        while True :
            keword = input('검색어를 입력하세요\n\n:')
            if not keword:
                os.system('cls')
                pyautogui.alert('검색어가 입력되지 않았습니다!')
                continue
            else :
                return keword

    # 타입체크 메서드
    @staticmethod
    def type_check(obj,typer):
        if isinstance(obj, typer):
            pass
        else:
            raise TypeError(f'{typer} :: Typer Error')


if __name__ == '__main__':
    app = GetNaverImage()

    # event loop 에러 제거
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(app.run())

