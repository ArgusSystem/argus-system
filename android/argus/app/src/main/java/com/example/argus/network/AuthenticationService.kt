package com.example.argus.network

import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

interface AuthenticationService {

    // Get from /users/<username>?password=<password>
    @GET("users/{username}")
    fun logIn(@Path("username") username : String,
              @Query("password") parameter : String) : Call<String>
}