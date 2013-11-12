//
//  DOCTask.h
//  Patient.ly
//
//  Created by Angie Lal on 11/8/13.
//  Copyright (c) 2013 Angie Lal. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface DOCTask : NSObject

@property (nonatomic, strong) NSNumber *tid;
@property (nonatomic, strong) NSString *name;
@property (nonatomic, strong) NSString *issue;
//@property (nonatomic, strong) NSDate *timestamp;

-(DOCTask *)initWithId:(NSNumber *)pid name:(NSString *)name issue:(NSString *)issue;
@end
