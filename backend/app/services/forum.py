from typing import List, Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from backend.app.models.forum import Post, Comment
from backend.app.schemas.forum import PostCreate, PostUpdate, CommentCreate

def get_posts(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    """获取所有帖子"""
    return db.query(Post).order_by(desc(Post.created_at)).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int) -> Optional[Post]:
    """获取特定帖子"""
    return db.query(Post).filter(Post.id == post_id).first()

def create_post(db: Session, post_in: PostCreate, user_id: int) -> Post:
    """创建新帖子"""
    post = Post(
        title=post_in.title,
        content=post_in.content,
        owner_id=user_id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def update_post(db: Session, post: Post, post_in: PostUpdate) -> Post:
    """更新帖子"""
    update_data = post_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)
    
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post_id: int) -> bool:
    """删除帖子"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return False
    
    db.delete(post)
    db.commit()
    return True

def get_comments(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
    """获取帖子的所有评论"""
    return db.query(Comment).filter(
        Comment.post_id == post_id,
        Comment.parent_id.is_(None)  # 只获取顶级评论
    ).order_by(Comment.created_at).offset(skip).limit(limit).all()

def create_comment(db: Session, comment_in: CommentCreate, user_id: int) -> Comment:
    """创建新评论"""
    comment = Comment(
        content=comment_in.content,
        owner_id=user_id,
        post_id=comment_in.post_id,
        parent_id=comment_in.parent_id
    )
    db.add(comment)
    
    # 更新帖子的评论计数
    post = db.query(Post).filter(Post.id == comment_in.post_id).first()
    if post:
        post.comment_count += 1
    
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, comment_id: int) -> bool:
    """删除评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return False
    
    # 更新帖子的评论计数 (减少主评论及其所有回复的数量)
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if post:
        # 计算要删除的评论总数 (主评论+所有回复)
        replies_count = db.query(Comment).filter(Comment.parent_id == comment_id).count()
        post.comment_count -= (1 + replies_count)  # 主评论 + 回复数
    
    db.delete(comment)
    db.commit()
    return True

def increment_post_view(db: Session, post_id: int) -> Post:
    """增加帖子浏览次数"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.view_count += 1
        db.commit()
        db.refresh(post)
    return post

def like_post(db: Session, post_id: int) -> Post:
    """点赞帖子"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.like_count += 1
        db.commit()
        db.refresh(post)
    return post 