from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class GameType(models.Model):
    """Types of legal games"""
    GAME_TYPES = [
        ('courtroom', 'Courtroom Simulation'),
        ('criminal_case', 'Criminal Case Analysis'),
        ('quiz', 'Legal Tests & Quizzes'),
        ('scenario', 'Correct or Incorrect Scenarios'),
    ]
    
    name = models.CharField(max_length=100)
    game_type = models.CharField(max_length=20, choices=GAME_TYPES)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Game(models.Model):
    """Individual game instances"""
    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE, related_name='games')
    title = models.CharField(max_length=200)
    description = models.TextField()
    scenario = models.TextField(help_text="Game scenario/story")
    points_per_question = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('games:game_detail', kwargs={'pk': self.pk})


class GameQuestion(models.Model):
    """Questions within a game"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=[
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('scenario', 'Scenario Decision'),
    ], default='multiple_choice')
    order = models.IntegerField(default=0)
    points = models.IntegerField(default=10)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.game.title} - Question {self.order}"


class GameAnswer(models.Model):
    """Answers for game questions"""
    question = models.ForeignKey(GameQuestion, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(blank=True, help_text="Explanation shown after answering")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.question} - {self.answer_text[:50]}"


class GameSession(models.Model):
    """User game session/attempt"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_sessions')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sessions')
    score = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.game.title}"


class GameAnswerSubmission(models.Model):
    """User's answer submissions"""
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='submissions')
    question = models.ForeignKey(GameQuestion, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(GameAnswer, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.session.user.username} - {self.question}"


class Leaderboard(models.Model):
    """Leaderboard entries"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard_entry')
    total_points = models.IntegerField(default=0)
    games_completed = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-total_points', 'last_updated']
    
    def __str__(self):
        return f"{self.user.username} - {self.total_points} points"


class MultiplayerGameRoom(models.Model):
    """Multiplayer game room for real-time courtroom simulations"""
    STATUS_CHOICES = [
        ('waiting', 'Waiting for Players'),
        ('ready', 'Ready to Start'),
        ('active', 'Game Active'),
        ('completed', 'Completed'),
    ]
    
    ROLE_CHOICES = [
        ('judge', 'Judge'),
        ('prosecutor', 'Prosecutor'),
        ('defense', 'Defense Attorney'),
        ('investigator', 'Investigator'),
    ]
    
    room_code = models.CharField(max_length=8, unique=True, help_text="Unique room code for joining")
    title = models.CharField(max_length=200)
    scenario = models.TextField(help_text="Courtroom scenario for the game")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mp_games_as_player1', null=True, blank=True)
    player1_role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mp_games_as_player2', null=True, blank=True)
    player2_role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    current_turn = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_turn_rooms')
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_games')
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Room {self.room_code} - {self.title}"
    
    def generate_room_code(self):
        """Generate a unique room code"""
        import random
        import string
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not MultiplayerGameRoom.objects.filter(room_code=code).exists():
                return code
    
    def save(self, *args, **kwargs):
        if not self.room_code:
            self.room_code = self.generate_room_code()
        super().save(*args, **kwargs)


class MultiplayerGameMove(models.Model):
    """Moves/actions in multiplayer game"""
    room = models.ForeignKey(MultiplayerGameRoom, on_delete=models.CASCADE, related_name='moves')
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    move_type = models.CharField(max_length=50, help_text="Type of move (question, argument, decision, etc.)")
    move_data = models.JSONField(help_text="Data for the move")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.player.username} - {self.move_type} - {self.room.room_code}"

