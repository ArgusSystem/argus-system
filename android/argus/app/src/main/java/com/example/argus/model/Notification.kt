package com.example.argus.model

import com.google.gson.annotations.SerializedName


data class WhenValue(
    @SerializedName("days")
    val days: List<String>,
    @SerializedName("end_time")
    val endTime: Int,
    @SerializedName("start_time")
    val startTime: Int,
    @SerializedName("time_zone")
    val timeZone: String
)

data class WhenCondition(
    @SerializedName("type")
    val type: String,
    @SerializedName("value")
    val value: WhenValue
)

data class WhereCondition(
    @SerializedName("type")
    val type: String,
    @SerializedName("value")
    val value: List<Int>
)

data class WhoCondition(
    @SerializedName("type")
    val type: String,
    @SerializedName("value")
    val value: List<Int>
)

data class Rule(
    @SerializedName("when")
    val whenConditions: List<WhenCondition>,
    @SerializedName("where")
    val whereConditions: List<WhereCondition>,
    @SerializedName("who")
    val whoConditions: List<WhoCondition>
)

data class Restriction(
    @SerializedName("rule")
    val rule: Rule,
    @SerializedName("severity")
    val severity: Int
)

data class Notification(
    @SerializedName("camera_id")
    val cameraId: Int,
    @SerializedName("end_time")
    val endTime: Long,
    @SerializedName("person")
    val person: String,
    @SerializedName("person_id")
    val personId: Int,
    @SerializedName("place")
    val place: String,
    @SerializedName("read")
    val read: Boolean,
    @SerializedName("restriction")
    val restriction: Restriction,
    @SerializedName("restriction_id")
    val restrictionId: Int,
    @SerializedName("start_time")
    val startTime: Long,
    @SerializedName("user_id")
    val userId: Int
)

data class NotificationStatus(
    @SerializedName("count")
    val count: Int,
    @SerializedName("latest")
    val latest: Long,
)