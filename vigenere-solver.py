import PySimpleGUI as sg

# 设置主题
sg.theme('SystemDefaultForReal')

def char_offset(char, offset):
    if offset < 0:
        offset += 26
    if char.islower():
        return chr((ord(char) - 97 + offset) % 26 + 97)
    else:
        return chr((ord(char) - 65 + offset) % 26 + 65)

def vigenere(str_in, key, encode):
    str_out = ""
    j = 0
    for c in str_in:
        if c.isalpha():
            offset = ord(key[j % len(key)]) - 97
            j += 1
            if not encode:
                offset = -offset
            str_out += char_offset(c, offset)
        else:
            str_out += c
    return str_out

def de_vigenere_auto(ciphertext):
    best_key = ""
    count = [0] * 26
    cipher_min = ''.join(filter(str.isalpha, ciphertext.lower()))
    freq = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 
            0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 
            6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]

    for key_len in range(3, 13):
        sum_ic = 0
        for j in range(key_len):
            count = [0] * 26
            for i in range(j, len(cipher_min), key_len):
                count[ord(cipher_min[i]) - 97] += 1
            ic = sum((count[i] / (len(cipher_min) / key_len)) ** 2 for i in range(26))
            sum_ic += ic
        if sum_ic / key_len > 0.065:
            break

    for j in range(key_len):
        count = [0] * 26
        for i in range(j, len(cipher_min), key_len):
            count[ord(cipher_min[i]) - 97] += 1

        max_dp = -1000000
        best_i = 0
        for i in range(26):
            cur_dp = sum(freq[k] * count[(k + i) % 26] for k in range(26))
            if cur_dp > max_dp:
                max_dp = cur_dp
                best_i = i
        best_key += chr(best_i + 97)

    return best_key

def main():
    layout = [
        [sg.Text('明文:')],
        [sg.Multiline(size=(80, 10), key='-INPUT-')],
        [sg.Text('密钥 (仅字母):'), sg.InputText(key='-KEY-')],
        [sg.Button('加密 ↓'), sg.Button('解密 ↑'), sg.Button('清空')],
        [sg.Text('密文:')],
        [sg.Multiline(size=(80, 10), key='-OUTPUT-')]
    ]

    window = sg.Window('vigenere-solver', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == '加密 ↓':
            try:
                plaintext = values['-INPUT-']
                key = values['-KEY-'].lower()
                if not key.isalpha():
                    sg.popup('密钥必须为字母!')
                    continue
                ciphertext = vigenere(plaintext, key, True)
                window['-OUTPUT-'].update(ciphertext)
            except Exception as e:
                sg.popup(str(e))

        if event == '解密 ↑':
            try:
                ciphertext = values['-OUTPUT-']
                key = values['-KEY-'].lower()
                if not key:
                    key = de_vigenere_auto(ciphertext)
                    window['-KEY-'].update(key)
                if not key.isalpha():
                    sg.popup('密钥必须为字母!')
                    continue
                plaintext = vigenere(ciphertext, key, False)
                window['-INPUT-'].update(plaintext)
            except Exception as e:
                sg.popup(str(e))
        if event == '清空':
            window['-INPUT-'].update('')
            window['-OUTPUT-'].update('')
            window['-KEY-'].update('')

    window.close()

if __name__ == '__main__':
    main()
