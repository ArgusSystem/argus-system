package com.example.argus.model

import com.google.gson.annotations.SerializedName

data class Restriction(
    @SerializedName("severity")
    val severity: Int = 0
)

data class Notification(
    @SerializedName("camera_id")
    val cameraId: Int = 0,
    @SerializedName("end_time")
    val endTime: Long = 0,
    @SerializedName("person")
    val person: String = "",
    @SerializedName("person_id")
    val personId: Int = 0,
    @SerializedName("place")
    val place: String = "",
    @SerializedName("read")
    var read: Boolean = false,
    @SerializedName("restriction")
    val restriction: Restriction = Restriction(),
    @SerializedName("restriction_id")
    val restrictionId: Int = 0,
    @SerializedName("start_time")
    val startTime: Long = 0,
    @SerializedName("user_id")
    val userId: Int = 0
)

data class NotificationStatus(
    @SerializedName("count")
    val count: Int = 0,
    @SerializedName("latest")
    val latest: Long = 0,
)