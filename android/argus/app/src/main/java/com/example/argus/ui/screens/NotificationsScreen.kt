package com.example.argus.ui.screens

import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.Card
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.example.argus.ArgusScreen
import com.example.argus.R
import com.example.argus.model.Notification
import com.example.argus.model.NotificationViewModel
import com.example.argus.model.NotificationsState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TopBar(
    refreshAction: () -> Unit,
    navigateUp: () -> Unit,
    modifier: Modifier = Modifier
) {
    TopAppBar(
        title = { Text(stringResource(ArgusScreen.Notifications.title)) },
        colors = TopAppBarDefaults.mediumTopAppBarColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        ),
        modifier = modifier,
        actions = {
                  IconButton(
                      onClick = refreshAction,
                      modifier = modifier.padding(end = 16.dp)) {
                        Icon(
                            imageVector = Icons.Filled.Refresh,
                            contentDescription = stringResource(R.string.refresh_button)
                        )
                  }
        },
        navigationIcon = {
            IconButton(onClick = navigateUp) {
                Icon(
                    imageVector = Icons.Filled.ArrowBack,
                    contentDescription = stringResource(R.string.back_button)
                )
            }
        }
    )
}

@Composable
fun NotificationsScreen(notificationViewModel: NotificationViewModel, navigateUp: () -> Unit, modifier: Modifier = Modifier) {
    Scaffold(
        topBar = {
            TopBar(
                refreshAction = { notificationViewModel.fetchNotifications() },
                navigateUp = navigateUp
            )
        }
    ) { innerPadding ->
        when (val notificationsState = notificationViewModel.notificationsState) {
            is NotificationsState.Loading -> LoadingScreen(modifier.padding(innerPadding))
            is NotificationsState.Success -> NotificationList(
                notificationsState.notifications,
                modifier.padding(innerPadding)
            )
        }
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