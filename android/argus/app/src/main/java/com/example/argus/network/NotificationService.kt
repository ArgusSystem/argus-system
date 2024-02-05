package com.example.argus.network

import com.example.argus.model.Notification
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

interface NotificationService {

    @GET("notifications/user/{username}")
    fun fetchNotifications(
        @Path("username") username : String,
        @Query("count") count : Int) : Call<List<Notification>>

    @GET("notifications/user/{username}/count")
    fun countNotifications(
        @Path("username") username : String) : Call<Int>

}