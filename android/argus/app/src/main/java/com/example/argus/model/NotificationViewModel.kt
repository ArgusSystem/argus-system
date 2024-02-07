package com.example.argus.model

import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import com.example.argus.data.NotificationClient
import com.example.argus.notifications.Manager
import java.util.concurrent.Executors
import java.util.concurrent.ScheduledFuture
import java.util.concurrent.TimeUnit

const val TAG = "Notifications"

sealed interface NotificationsState {
    data class Success(val notifications: List<Notification>) : NotificationsState
    data object Loading : NotificationsState
}


class NotificationViewModel(private val user : String, private val notificationClient: NotificationClient, private val notificationManager: Manager) : ViewModel() {
    var notificationsState: NotificationsState by mutableStateOf(NotificationsState.Loading)
        private set

    var newNotificationsCount: Int by mutableIntStateOf(0)
        private set

    private val notificationsFetchCount = 20

    private val executor = Executors.newSingleThreadScheduledExecutor()
    private var refreshFuture : ScheduledFuture<*>
    private var notifyFuture : ScheduledFuture<*>

    private var lastNotificationStatus : NotificationStatus? = null

    init {
        refresh()
        refreshFuture = scheduleRefresh()
        notifyFuture = scheduleNotify()
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
    }

    private fun scheduleRefresh(): ScheduledFuture<*> {
        return executor.scheduleAtFixedRate({
            refresh()
            Log.i(TAG, "Refreshed notifications in executor!")
         }, 30, 30, TimeUnit.SECONDS)
    }

    private fun scheduleNotify(): ScheduledFuture<*> {
        return executor.scheduleAtFixedRate({
            notificationClient.status(user, onStatus = { notificationStatus ->
                if (lastNotificationStatus != null) {
                    if (notificationStatus.latest > lastNotificationStatus!!.latest) {
                        notificationManager.sendNotification(
                            "New trespassing detected!",
                            "You have ${notificationStatus.count} unread notifications!")
                    }
                }

                lastNotificationStatus = notificationStatus
            })

            Log.i(TAG, "Notified in executor!")
        }, 60, 60, TimeUnit.SECONDS)
    }

    fun forceRefresh() {
        if (!refreshFuture.cancel(false)) {
            refresh()
            refreshFuture = scheduleRefresh()
        }
    }
}