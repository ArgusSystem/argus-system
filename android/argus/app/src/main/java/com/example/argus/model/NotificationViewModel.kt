package com.example.argus.model

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import com.example.argus.data.NotificationClient

sealed interface NotificationsState {
    data class Success(val notifications: List<Notification>) : NotificationsState
    data object Loading : NotificationsState
}


class NotificationViewModel(private val user : String, private val notificationClient: NotificationClient) : ViewModel() {
    var notificationsState: NotificationsState by mutableStateOf(NotificationsState.Loading)
        private set

    private val notificationsFetchCount = 10

    init {
        fetchNotifications()
    }

    fun fetchNotifications() {
        notificationsState = NotificationsState.Loading

        notificationClient.fetch(user, notificationsFetchCount) { notifications ->
            notificationsState = NotificationsState.Success(notifications)
        }
    }
}