package com.example.argus.data

import com.example.argus.network.AuthenticationService
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.converter.scalars.ScalarsConverterFactory

class AuthenticationClient {

    private val BASE_URL = "http://argus:5000/"

    private val retrofit: Retrofit = Retrofit.Builder()
        .addConverterFactory(ScalarsConverterFactory.create())
        .baseUrl(BASE_URL)
        .build()

    private val service: AuthenticationService by lazy {
        retrofit.create(AuthenticationService::class.java)
    }

    fun logIn(username : String, password : String) : String? {
        val call = service.logIn(username, password)

        val response = call.execute()

        if (response.isSuccessful) {
            return response.body()
        }

        return null
    }
}