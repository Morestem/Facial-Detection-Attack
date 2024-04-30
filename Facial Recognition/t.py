import cv2, re
import face_recognition as fr

def takephoto(login):
    camera = cv2.VideoCapture(0)
    print("Pressione 'f' para registrar sua foto")
    while True:
        _, frame = camera.read()
        cv2.imshow("Pressione 'f' para registrar sua foto", frame)
        key = cv2.waitKey(1)
        if key == ord('f'): 
            cv2.imwrite(r"C:\Users\joaom\OneDrive\Desktop\Facial Recognition\users\userphoto/" + login + ".png", frame)
            print("foto salva")
            break
        elif key == 27:
            print("Operação cancelada")
            break
    camera.release()
    cv2.destroyAllWindows()

def comparephoto(login):
    camera = cv2.VideoCapture(0)
    print("Pressione 'f' para fazer o reconhecimento facial")
    while True:
        _, frame = camera.read()
        cv2.imshow("Pressione 'f' para fazer o reconhecimento facial", frame)
        key = cv2.waitKey(1)
        if key == ord('f'): 
            cv2.imwrite(r"C:\Users\joaom\OneDrive\Desktop\Facial Recognition\users\authentification\temp" + ".png", frame)
            
            imagem_banco = fr.load_image_file(r"C:\Users\joaom\OneDrive\Desktop\Facial Recognition\users\userphoto/" + login + ".png")
            imagem_banco = cv2.cvtColor(imagem_banco,cv2.COLOR_BGR2RGB)
            imagem_nova = fr.load_image_file(r"C:\Users\joaom\OneDrive\Desktop\Facial Recognition\users\authentification\temp" + ".png")
            imagem_nova = cv2.cvtColor(imagem_nova,cv2.COLOR_BGR2RGB)

            faceLoc = fr.face_locations(imagem_banco)[0]
            cv2.rectangle(imagem_banco,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(0,255,0),2)

            encode_imagem_banco = fr.face_encodings(imagem_banco)[0]
            encode_imagem_nova = fr.face_encodings(imagem_nova)[0]

            comparacao = fr.compare_faces([encode_imagem_banco],encode_imagem_nova)
            distancia = fr.face_distance([encode_imagem_banco],encode_imagem_nova)

            return (comparacao, distancia)

        elif key == 27:
            print("Operação cancelada")
            break
    camera.release()
    cv2.destroyAllWindows()

def main():
    login_user_folder_escrita = open(r"C:\Users\joaom\OneDrive\Desktop\Facial Recognition\users\userlogin.txt", "a")
    login_user_folder_leitura = open(r"C:\Users\joaom\OneDrive\Desktop\Facial Recognition\users\userlogin.txt", "r")
    usuarios_e_senhas = login_user_folder_leitura.readlines()
    logins, senhas = [], []
    padrao = r'(\S+)\s+(\S+)'
    for item in usuarios_e_senhas:
        match = re.match(padrao, item)
        if match:
            login = match.group(1)
            senha = match.group(2)
            logins.append(login)
            senhas.append(senha)

    cadastro = input("Bem-vindo(a) ao sistema\n\n Já possui cadastro?(y/n) ")
    if cadastro != "y":
        if input("Deseja cadastrar-se?(y/n) ") != "y":
            exit()
        else:
            login_novo_usuario = input("Informe seu nome: ")
            senha_novo_usuario = input("informe uma senha para sua conta: ")
            login_user_folder_escrita.writelines(login_novo_usuario + " " + senha_novo_usuario + "\n")
            takephoto(login_novo_usuario)
    else:
        login_usuario = input("Informe seu login: ")
        senha_usuario = input("Informe sua senha: ")
        if login_usuario not in logins:
            print("Login errado")
            exit()
        else:
            login_index = logins.index(login_usuario)
        if senha_usuario != senhas[login_index]:
            print("Senha errada")
            exit()
        else:
            comparacao, distancia = comparephoto(login)
            print(comparacao,distancia)
            if distancia[0] < 0.55:
                print("Bem-vindo")
            else:
                print("Impostor!")

def modelattack():
    pass

if __name__ == '__main__':
    main()