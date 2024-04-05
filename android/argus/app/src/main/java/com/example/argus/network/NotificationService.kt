package com.example.argus.network

import com.example.argus.model.Notification
import com.example.argus.model.NotificationFace
import com.example.argus.model.NotificationStatus
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.POST
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

    @GET("notifications/user/{username}/status")
    fun fetchNotificationStatus(
        @Path("username") username : String) : Call<NotificationStatus>

    @POST("notifications/id/{userId}/{cameraId}/{personId}/{restrictionId}/{startTime}/read")
    fun markNotificationRead(
        @Path("userId") userId : Int,
        @Path("cameraId") cameraId : Int,
        @Path("personId") personId : Int,
        @Path("restrictionId") restrictionId : Int,
        @Path("startTime") startTime: Long) : Call<Boolean>

    @GET("notifications/id/{userId}/{cameraId}/{personId}/{restrictionId}/{startTime}/faces")
    fun fetchNotificationFaces(
        @Path("userId") userId : Int,
        @Path("cameraId") cameraId : Int,
        @Path("personId") personId : Int,
        @Path("restrictionId") restrictionId : Int,
        @Path("startTime") startTime: Long) : Call<List<NotificationFace>>
}