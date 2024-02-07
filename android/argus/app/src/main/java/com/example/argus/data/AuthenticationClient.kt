package com.example.argus.data

import android.util.Log
import androidx.compose.ui.res.stringResource
import com.example.argus.R
import com.example.argus.network.AuthenticationService
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.converter.scalars.ScalarsConverterFactory

class AuthenticationClient {

    private val BASE_URL = "http://192.168.0.17:5000/"
    private val TAG = "AuthenticationClient"

    private val retrofit: Retrofit = Retrofit.Builder()
        .addConverterFactory(ScalarsConverterFactory.create())
        .baseUrl(BASE_URL)
        .build()

    private val service: AuthenticationService by lazy {
        retrofit.create(AuthenticationService::class.java)
    }

    fun logIn(username : String, password : String, onSuccess : (String) -> Unit, onFailure : (String) -> Unit) {
        val call = service.logIn(username, password)

        call.enqueue(object : Callback<String> {
            override fun onResponse(call: Call<String>, response: Response<String>) {
                if (response.isSuccessful) {
                    val alias = response.body()
                    onSuccess(alias!!)
                } else {
                    onFailure("Invalid username or password")
                }
            }

            override fun onFailure(call: Call<String>, t: Throwable) {
                onFailure("Internal server error")
            }
        })
    }
}