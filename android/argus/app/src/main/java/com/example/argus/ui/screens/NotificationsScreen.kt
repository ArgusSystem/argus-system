package com.example.argus.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.Badge
import androidx.compose.material3.BadgedBox
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.argus.ArgusScreen
import com.example.argus.R
import com.example.argus.model.Notification
import com.example.argus.model.NotificationViewModel
import com.example.argus.model.NotificationsState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TopBar(
    notificationViewModel: NotificationViewModel,
    navigateUp: () -> Unit,
    modifier: Modifier = Modifier
) {
    TopAppBar(
        title = {
            BadgedBox(badge = {
                Badge(containerColor = Color.Red, contentColor = Color.White)  {
                    Text(text = notificationViewModel.newNotificationsCount.toString())
                }
            }) {
                Text(stringResource(ArgusScreen.Notifications.title))
            }},
        colors = TopAppBarDefaults.mediumTopAppBarColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        ),
        modifier = modifier,
        actions = {
            IconButton(
                onClick = { notificationViewModel.forceRefresh() }) {
                Icon(
                    imageVector = Icons.Filled.Refresh,
                    contentDescription = stringResource(R.string.refresh_button)
                )
            }
        },
        navigationIcon = {
            IconButton(onClick = {
                notificationViewModel.cancel()
                navigateUp()
            }) {
                Icon(
                    imageVector = Icons.Filled.ArrowBack,
                    contentDescription = stringResource(R.string.back_button)
                )
            }
        }
    )
}

@Composable
fun NotificationsScreen(factory: ViewModelProvider.Factory, navigateUp: () -> Unit, onNotificationClick: (Notification) -> Unit, modifier: Modifier = Modifier) {
    val notificationViewModel: NotificationViewModel = viewModel(factory=factory)

    Scaffold(
        topBar = {
            TopBar(
                notificationViewModel = notificationViewModel,
                navigateUp = navigateUp
            )
        }
    ) { innerPadding ->
        when (val notificationsState = notificationViewModel.notificationsState) {
            is NotificationsState.Loading -> LoadingScreen(modifier.fillMaxSize())
            is NotificationsState.Success -> NotificationList(
                notificationsState.notifications,
                onNotificationClick = onNotificationClick,
                modifier.padding(innerPadding)
            )
        }
    }
}

@Composable
fun NotificationList(notifications: List<Notification>, onNotificationClick: (Notification) -> Unit, modifier: Modifier = Modifier) {
    LazyColumn(modifier = modifier) {
        items(notifications) { notification ->
            NotificationCard(notification = notification, onClick = onNotificationClick, modifier = Modifier.padding(8.dp))
        }
    }
}

@Composable
fun NotificationCard(notification: Notification, onClick: (Notification) -> Unit, modifier: Modifier = Modifier) {
    val fontWeight = if (notification.read) FontWeight.Normal else FontWeight.Bold

    val containerColor = when (notification.restriction.severity) {
        0 -> Color.LightGray
        1 -> Color(255, 246, 0)
        2 -> Color(225, 90, 70)
        else -> Color.White
    }

    Card(colors = CardDefaults.cardColors(
        containerColor = containerColor
    ), modifier = modifier.clickable {
        onClick(notification)
    }) {
        Text(
            text = stringResource(
                R.string.unauthorized_person,
                notification.place,
                notification.person
            ),
            modifier = Modifier.padding(16.dp),
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = fontWeight
        )
    }
}