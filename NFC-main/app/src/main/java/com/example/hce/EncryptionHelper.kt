package com.example.hce

import javax.crypto.Cipher
import javax.crypto.SecretKey
import javax.crypto.spec.IvParameterSpec
import javax.crypto.spec.SecretKeySpec

object EncryptionHelper {

    private const val AES_ALGORITHM = "AES"
    private const val AES_TRANSFORMATION = "AES/ECB/PKCS5Padding"
    private val SECRET_KEY = KeyGeneratorHelper.generateRandomKey()

    fun aesEncrypt(data: ByteArray, secretKey: SecretKey,iv: IvParameterSpec): ByteArray {
        val cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, iv)
        return cipher.doFinal(data)
    }
}

