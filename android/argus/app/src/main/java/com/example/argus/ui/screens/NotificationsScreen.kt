package com.example.argus.ui.screens

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
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.argus.ArgusScreen
import com.example.argus.R
import com.example.argus.data.NotificationClient
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
fun NotificationsScreen(factory: ViewModelProvider.Factory, navigateUp: () -> Unit, modifier: Modifier = Modifier) {
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