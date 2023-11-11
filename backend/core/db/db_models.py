from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DateTime, Float, Numeric, SmallInteger, BigInteger, JSON, Boolean, CheckConstraint, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import JSONB
import datetime, json, random


DeclBase = declarative_base()

class User(DeclBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    #TODO: finish

class StatIip(DeclBase):
    __tablename__ = "stat_tips"

    id = Column(Integer, primary_key=True)
    min_level = Column(SmallInteger, default=0)
    max_level = Column(SmallInteger, default=30)
    tips = Column(JSON)
    other_data = Column(JSON, default={})

    __table_args__ = (
        #same constraints as in StatTips class
        CheckConstraint("min_level >= 0", name="check_minimum_tips_min_level"),
        CheckConstraint("min_level <= 100", name="check_maximum_tips_min_level"),

        CheckConstraint("max_level >= 0", name="check_minimum_tips_max_level"),
        CheckConstraint("max_level <= 100", name="check_maximum_tips_max_level"),

        CheckConstraint("max_level >= min_level", name="check_range_tips"),
    )

class Stat(DeclBase):
    __tablename__ = "stats"

    display_name = Column(String(64))
    icon_base_name = Column(String(256))
    #TODO: rework to work like get all in tips.stat_id == self.id
    tips_id = Column(Integer, ForeignKey('stat_tips.id'))
    exp_requirement_mult = Column(Numeric(precision=6, scale=5), default=1.3)
    exp_requirement_flat_bonus = Column(Integer, default=150)
    level_base_requirement = Column(Integer, default=100)
    exp = Column(BigInteger, default=0)
    asociated_tasks = relationship("Task", secondary="task_stat_association", back_populates='stats')

    user_profile_id = Column(Integer, ForeignKey('user_profiles.id'))
    
    other_data = Column(JSON, default={})
    
    __table_args__ = (
        #same constraints as in Stat class
        CheckConstraint("length(display_name) >= 3", name="check_min_display_name_length"),
        CheckConstraint("length(display_name) <= 64", name="check_max_display_name_length"),

        #TODO: write check for if the icon is not in icon table
        CheckConstraint("exp_requirement_mult >= 1", name="check_min_exp_mult"),
        CheckConstraint("exp_requirement_mult < 10", name="check_max_exp_mult"),

        CheckConstraint("exp_requirement_flat_bonus >= 0", name="check_min_exp_requirement_flat_bonus"),
        CheckConstraint("exp_requirement_flat_bonus <= 999999", name="check_max_exp_requirement_flat_bonus"),

        CheckConstraint("level_base_requirement >= 0", name="check_min_level_base_requirement"),
        CheckConstraint("level_base_requirement <= 999999", name="check_max_level_base_requirement"),
        
        CheckConstraint("exp >= 0", name="check_min_exp"),
        CheckConstraint("exp <= 999999999999", name="check_max_exp")
    )

class UserProfile(DeclBase):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    asociated_tasks = relationship('Task', back_populates='user_profiles')
    asociated_stats = relationship('Stat', back_populates='user_profiles')
    #TODO: finish

class Task(DeclBase):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    display_name = Column(String(128), nullable=False)
    asociated_stats = relationship("Stat", secondary="task_stat_association", back_populates='tasks')
    description = Column(String(30000), default='Add more info about your task')
    difficulty_modifier = Column(Float, default=1.0)
    time_modifier = Column(Float, default=1.0)
    base_exp_reward = Column(Integer, default=10)
    due_date = Column(DateTime)
    due_date_penalty = Column(Float, default=0.25)

    user_profile_id = Column(Integer, ForeignKey('user_profiles.id'))
    other_data = Column(JSON, default={})

    __table_args__ = (
        #same constraints as in Task class
        CheckConstraint("length(display_name) >= 3", name="check_min_display_name_length"),
        CheckConstraint("length(display_name) <= 128", name="check_max_display_name_length"),

        CheckConstraint("length(description) >= 0", name="check_min_description_length"),
        CheckConstraint("length(description) <= 30000", name="check_max_description_length"),

        CheckConstraint("difficulty_modifier >= 0", name="check_min_difficulty_modifier"),
        CheckConstraint("difficulty_modifier <= 100", name="check_max_difficulty_modifier"),

        CheckConstraint("time_modifier >= 0", name="check_min_time_modifier"),
        CheckConstraint("time_modifier <= 100", name="check_max_time_modifier"),

        CheckConstraint("base_exp_reward >= 0", name="check_min_base_exp_reward"),
        CheckConstraint("base_exp_reward <= 99999", name="check_max_base_exp_reward"),

        CheckConstraint("due_date_penalty >= 0", name="check_min_due_date_penalty"),
        CheckConstraint("due_date_penalty <= 1", name="check_max_due_date_penalty"),
    )

    # Define a foreign key relationship to the Stat table
    stat_id = Column(Integer, ForeignKey('stats.id'))

task_stat_association = Table(
    'task_stat_association',
    DeclBase.metadata,
    Column('task', Integer, ForeignKey('task.id')),
    Column('stat', Integer, ForeignKey('stat.id')), 
    Column('mult', Numeric(precision=6, scale=5))
)