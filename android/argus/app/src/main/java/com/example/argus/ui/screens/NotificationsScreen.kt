package com.example.argus.ui.screens

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.argus.R
import com.example.argus.data.NotificationClient
import com.example.argus.model.Notification
import com.example.argus.model.NotificationViewModel
import com.example.argus.model.NotificationsState

@Composable
fun NotificationsScreen(notificationViewModel: NotificationViewModel, modifier: Modifier = Modifier) {
    val notificationsState = notificationViewModel.notificationsState

    when (notificationsState) {
        is NotificationsState.Loading -> LoadingScreen(modifier.fillMaxSize())
        is NotificationsState.Success -> NotificationList(notificationsState.notifications, modifier.fillMaxWidth())
    }
}

@Composable
fun NotificationList(notifications: List<Notification>, modifier: Modifier = Modifier) {
    LazyColumn(modifier = modifier) {
        items(notifications) { notification ->
            NotificationCard(notification = notification, modifier = Modifier.padding(8.dp))
        }
    }
}

@Composable
fun NotificationCard(notification: Notification, modifier: Modifier = Modifier) {
    Card(modifier = modifier) {
        Text(
            text = stringResource(
                R.string.unauthorized_person,
                notification.place,
                notification.person
            ),
            modifier = Modifier.padding(16.dp),
            style = MaterialTheme.typography.headlineSmall
        )
    }
}