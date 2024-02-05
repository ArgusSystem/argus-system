package com.example.argus.model

import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import com.example.argus.data.NotificationClient
import java.util.concurrent.Executors
import java.util.concurrent.ScheduledExecutorService
import java.util.concurrent.ScheduledFuture
import java.util.concurrent.TimeUnit

const val TAG = "Notifications"

sealed interface NotificationsState {
    data class Success(val notifications: List<Notification>) : NotificationsState
    data object Loading : NotificationsState
}


class NotificationViewModel(private val user : String, private val notificationClient: NotificationClient) : ViewModel() {
    var notificationsState: NotificationsState by mutableStateOf(NotificationsState.Loading)
        private set

    var newNotificationsCount: Int by mutableStateOf(0)
        private set

    private val notificationsFetchCount = 10

    private val executor = Executors.newSingleThreadScheduledExecutor()
    private var scheduledFuture : ScheduledFuture<*>

    init {
        refresh()
        scheduledFuture = scheduleRefresh()
    }

    private fun fetchNotifications() {
        notificationClient.fetch(user, notificationsFetchCount) { notifications ->
            notificationsState = NotificationsState.Success(notifications)
        }
    }

    private fun fetchNewNotificationsCount() {
        notificationClient.count(user) { count ->
            newNotificationsCount = count
        }
    }

    private fun refresh() {
        notificationsState = NotificationsState.Loading

        fetchNewNotificationsCount()
        fetchNotifications()

        Log.i(TAG, "Refreshed notifications!")
    }

    private fun scheduleRefresh(): ScheduledFuture<*> {
        return executor.schedule({ refresh() }, 1, TimeUnit.MINUTES)
    }

    fun forceRefresh() {
        scheduledFuture.cancel(false)
        refresh()
        scheduledFuture = scheduleRefresh()
    }
}