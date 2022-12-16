##############################################
# <실습6> 챗봇 전처리 모듈(클래스) 
##############################################

from konlpy.tag import Komoran
import pickle

class Preprocess:
    def __init__(self, word2index_dic='', userdic=None):
        
        # 단어 인덱스 사전 불러오기 (실습10에서 추가)
        if(word2index_dic != ''):      # /train_tools/dict/create_dict.ipynb에서 만든
            f = open(word2index_dic, "rb")
            self.word_index = pickle.load(f)   # 단어사전 딕셔너리
            f.close()
        else:
            self.word_index = None
        
        # 형태소 분석기 초기화 (사용자 사전을 option활용)
        self.komoran = Komoran(userdic=userdic)
        
        # 제외할 품사
        # 참조 : https://docs.komoran.kr/firststep/postypes.html
        # 관계언 제거, 기호 제거
        # 어미 제거
        # 접미사 제거
        self.exclusion_tags = [
            'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ',   # 조사
            'JX', 'JC',
            'SF', 'SP', 'SS', 'SE', 'SO',                      # 기호
            'EP', 'EF', 'EC', 'ETN', 'ETM',                    # 어미
            'XSN', 'XSV', 'XSA'                                # 접미사
        ]
        
    # 형태소(품사) 분석기 POS 태거
    def pos(self, sentence):
        return self.komoran.pos(sentence)
        
    # 불용어 제거 후, 필요한 품사 정보만 가져오기
    def get_keywords(self, pos, without_tag=False):
        f = lambda x: x in self.exclusion_tags  # 불용어 사전에 있으면 True
        word_list = []
        for p in pos:
            if f(p[1]) is False:   # 함수에서 받은 품사가 불용어가 아닐때...
                word_list.append(p if without_tag is False else p[0])
                # without_tag가 True이면 품사태그 없이, False이면 (단어, 품사) 리스트 만들기
        return word_list
        
    #######################################################################
    # <실습10> 나중에 추가된 함수
    # 키워드를 단어 인덱스 시퀀스로 변환 (예제 8-5에서 추가)
    #######################################################################
    def get_wordidx_sequence(self, keywords):
        if self.word_index is None:
            return []
        
        w2i = []
        for word in keywords: # p = Preprocess() 로 인스턴스 만들때 
                              # option으로 준 파일을 읽어서 w2i 리스트 만들어줌
            try:
                w2i.append(self.word_index[word])   # 문장을 시퀀스 벡터로 
                
            except KeyError:
                # 해당 단어가 사전에 없는 경우, OOV 처리
                w2i.append(self.word_index['OOV'])   # 
                
        return w2i
        
        
        