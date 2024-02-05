package com.example.argus.data

import android.util.Log
import com.example.argus.model.Notification
import com.example.argus.network.NotificationService
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class NotificationClient(host: String, port: Int) {

    private val retrofit: Retrofit = Retrofit.Builder()
        .addConverterFactory(GsonConverterFactory.create())
        .baseUrl("http://$host:$port/")
        .build()

    private val service: NotificationService by lazy {
        retrofit.create(NotificationService::class.java)
    }

    fun fetch(user: String, count: Int, onNotifications: (List<Notification>) -> Unit) {
        val call = service.fetchNotifications(user, count)

        call.enqueue(object : Callback<List<Notification>> {
            override fun onResponse(call: Call<List<Notification>>, response: Response<List<Notification>>) {
                if (response.isSuccessful) {
                    onNotifications(response.body()!!)
                }
            }

            override fun onFailure(call: Call<List<Notification>>, t: Throwable) {
                Log.e(javaClass.simpleName, "Failed to fetch notifications!", t)
            }
        })
    }

    fun count(user: String, onNotificationsCount: (Int) -> Unit) {
        val call = service.countNotifications(user)

        call.enqueue(object : Callback<Int> {
            override fun onResponse(call: Call<Int>, response: Response<Int>) {
                if (response.isSuccessful) {
                    onNotificationsCount(response.body()!!)
                }
            }

            override fun onFailure(call: Call<Int>, t: Throwable) {
                Log.e(javaClass.simpleName, "Failed to fetch new notifications count!", t)
            }
        })
    }

}