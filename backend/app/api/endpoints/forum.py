from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.api import deps
from backend.app.services import forum as forum_service
from backend.app.schemas.forum import Post, PostCreate, PostUpdate, Comment, CommentCreate, PostWithComments
from backend.app.schemas.user import User

router = APIRouter()

@router.get("/posts", response_model=List[Post])
def get_posts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user)
):
    """
    获取所有帖子
    """
    return forum_service.get_posts(db, skip=skip, limit=limit)

@router.post("/posts", response_model=Post)
def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: PostCreate,
    current_user = Depends(deps.get_current_user)
):
    """
    创建新帖子
    """
    return forum_service.create_post(db, post_in, current_user.id)

@router.get("/posts/{post_id}", response_model=PostWithComments)
def get_post(
    post_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    获取特定帖子及其评论
    """
    post = forum_service.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail="帖子不存在"
        )
    
    # 增加浏览次数
    forum_service.increment_post_view(db, post_id)
    
    return post

@router.put("/posts/{post_id}", response_model=Post)
def update_post(
    post_id: int,
    *,
    db: Session = Depends(deps.get_db),
    post_in: PostUpdate,
    current_user = Depends(deps.get_current_user)
):
    """
    更新帖子
    """
    post = forum_service.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail="帖子不存在"
        )
    
    if post.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="无权修改此帖子"
        )
    
    return forum_service.update_post(db, post, post_in)

@router.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    删除帖子
    """
    post = forum_service.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail="帖子不存在"
        )
    
    if post.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="无权删除此帖子"
        )
    
    forum_service.delete_post(db, post_id)
    return {"status": "success"}

@router.post("/posts/{post_id}/like")
def like_post(
    post_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    点赞帖子
    """
    post = forum_service.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail="帖子不存在"
        )
    
    forum_service.like_post(db, post_id)
    return {"status": "success"}

@router.post("/comments", response_model=Comment)
def create_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_in: CommentCreate,
    current_user = Depends(deps.get_current_user)
):
    """
    创建评论
    """
    # 检查帖子是否存在
    post = forum_service.get_post(db, comment_in.post_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail="帖子不存在"
        )
    
    # 如果有父评论，检查父评论是否存在
    if comment_in.parent_id:
        parent_comment = db.query(Comment).filter(Comment.id == comment_in.parent_id).first()
        if not parent_comment:
            raise HTTPException(
                status_code=404,
                detail="父评论不存在"
            )
    
    return forum_service.create_comment(db, comment_in, current_user.id)

@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    删除评论
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=404,
            detail="评论不存在"
        )
    
    if comment.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="无权删除此评论"
        )
    
    forum_service.delete_comment(db, comment_id)
    return {"status": "success"} 