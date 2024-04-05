package com.example.argus.model

import com.google.gson.annotations.SerializedName

data class NotificationFace(
    @SerializedName("id")
    val id: Int = 0,
    @SerializedName("timestamp")
    val timestamp: Long = 0,
    @SerializedName("image_key")
    val imageKey: String = ""
)