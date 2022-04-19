from cryptography.fernet import Fernet


inputFile = input('Enter the file name you want to Encrypt / Decrypt  ')


userChoice = input('Do you want to Encrpyt (E) or Decrypt the file (D)')

if userChoice == 'E':
    key = Fernet.generate_key()
    with open('mykey.key', 'wb') as mykey:
        mykey.write(key)

    with open('mykey.key', 'rb') as mykey:
        key = mykey.read()

    f = Fernet(key)
    with open(inputFile, 'rb') as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original)
    with open("Enc_" + inputFile, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

if userChoice == 'D':

    with open('mykey.key', 'rb') as mykey:
        key = mykey.read()

    f = Fernet(key)
    with open("Enc_" + inputFile, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
        print('Encrypted')
    decrypted = f.decrypt(encrypted)

    # WRITE THE DECRYPTED FILE TO A NEW FILE
    with open("Dec_" + inputFile, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
